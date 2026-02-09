"""
============================================
Flask Application - Natural Language to SQL
============================================
Main Flask application that provides REST API endpoints
for converting natural language to SQL queries.

Author: AI Integration Project
"""

import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import custom modules
from db import db_manager, test_db_connection, execute_sql, execute_manual_sql, get_schema_context
from ai_service import ai_service, convert_to_sql

# Load environment variables
load_dotenv()

# ============================================
# Flask Application Setup
# ============================================

app = Flask(__name__)

# Enable CORS for all routes (allowing React frontend to connect)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'nl2sql_secret_key')
app.config['JSON_SORT_KEYS'] = False


# ============================================
# API Routes
# ============================================

@app.route('/')
def home():
    """Root endpoint - API information."""
    return jsonify({
        "name": "Natural Language to SQL API",
        "version": "1.0.0",
        "description": "Convert natural language prompts to SQL queries",
        "endpoints": {
            "POST /api/prompt": "Convert natural language to SQL and execute",
            "GET /api/health": "Health check endpoint",
            "GET /api/schema": "Get database schema information",
            "GET /api/examples": "Get example prompts"
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Returns the status of the API and database connection.
    """
    # Test database connection
    db_connected, db_message = test_db_connection()
    
    # Check AI service configuration
    ai_configured = (
        (ai_service.provider == 'openai' and ai_service.openai_key and ai_service.openai_key != 'your_openai_api_key_here') or
        (ai_service.provider == 'gemini' and ai_service.gemini_key and ai_service.gemini_key != 'your_gemini_api_key_here')
    )
    
    return jsonify({
        "status": "healthy" if db_connected else "degraded",
        "database": {
            "connected": db_connected,
            "message": db_message
        },
        "ai_service": {
            "provider": ai_service.provider,
            "configured": ai_configured
        }
    })


@app.route('/api/schema', methods=['GET'])
def get_schema():
    """
    Get the database schema.
    Returns table and column information.
    """
    try:
        schema = db_manager.get_table_schema()
        return jsonify({
            "success": True,
            "schema": schema
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """
    Get example prompts for the UI.
    """
    examples = [
        {
            "prompt": "Show all employees",
            "description": "Basic query to list all employee records"
        },
        {
            "prompt": "Provide employees data over 18 years age",
            "description": "Filter employees by age condition"
        },
        {
            "prompt": "Find employees with salary greater than 70000",
            "description": "Filter employees by salary"
        },
        {
            "prompt": "List employees in the Engineering department",
            "description": "Filter by department name"
        },
        {
            "prompt": "Show employees sorted by salary in descending order",
            "description": "Ordering results"
        },
        {
            "prompt": "Get the top 5 highest paid employees",
            "description": "Limiting results with ordering"
        },
        {
            "prompt": "Count employees in each department",
            "description": "Aggregation with GROUP BY"
        },
        {
            "prompt": "Find employees working on the Cloud Migration project",
            "description": "Query with JOIN across tables"
        },
        {
            "prompt": "Show all active employees hired after 2020",
            "description": "Multiple conditions with date filtering"
        },
        {
            "prompt": "List departments with their total employee count",
            "description": "JOIN with aggregation"
        }
    ]
    
    return jsonify({
        "success": True,
        "examples": examples
    })


@app.route('/api/prompt', methods=['POST'])
def process_prompt():
    """
    Main endpoint - Convert natural language to SQL and execute.
    
    Request Body:
        {
            "prompt": "Your natural language query here"
        }
    
    Response:
        {
            "success": true/false,
            "sql": "Generated SQL query",
            "data": [...results...],
            "row_count": number,
            "message": "Status message"
        }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided",
                "sql": None,
                "data": None
            }), 400
        
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({
                "success": False,
                "error": "Empty prompt provided. Please enter a query.",
                "sql": None,
                "data": None
            }), 400
        
        # Step 1: Get database schema context for AI
        schema_context = get_schema_context()
        
        if not schema_context or "Unable to retrieve" in schema_context:
            return jsonify({
                "success": False,
                "error": "Failed to retrieve database schema. Please check database connection.",
                "sql": None,
                "data": None
            }), 500
        
        # Step 2: Convert natural language to SQL using AI
        ai_success, sql_query, ai_message = convert_to_sql(prompt, schema_context)
        
        if not ai_success:
            return jsonify({
                "success": False,
                "error": f"AI Error: {ai_message}",
                "sql": sql_query if sql_query else None,
                "data": None
            }), 400
        
        # Step 3: Execute the SQL query
        db_success, results, db_message = execute_sql(sql_query)
        
        if not db_success:
            return jsonify({
                "success": False,
                "error": f"Database Error: {db_message}",
                "sql": sql_query,
                "data": None
            }), 400
        
        # Step 4: Return successful response
        return jsonify({
            "success": True,
            "sql": sql_query,
            "data": results,
            "row_count": len(results),
            "message": f"Query executed successfully. {len(results)} rows returned."
        })
        
    except Exception as e:
        # Log the error
        print(f"❌ Error processing prompt: {str(e)}")
        
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}",
            "sql": None,
            "data": None
        }), 500


@app.route('/api/raw-query', methods=['POST'])
def execute_raw_query():
    """
    Execute a raw SQL query (for testing purposes).
    Still validates that only SELECT queries are allowed.
    
    Request Body:
        {
            "sql": "SELECT * FROM employees;"
        }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('sql'):
            return jsonify({
                "success": False,
                "error": "No SQL query provided"
            }), 400
        
        sql_query = data.get('sql', '').strip()
        
        # Validate the query (using AI service's validation)
        is_valid, validation_message = ai_service.validate_sql(sql_query)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "error": f"Invalid query: {validation_message}",
                "sql": sql_query
            }), 400
        
        # Execute the query
        success, results, message = execute_sql(sql_query)
        
        if not success:
            return jsonify({
                "success": False,
                "error": message,
                "sql": sql_query
            }), 400
        
        return jsonify({
            "success": True,
            "sql": sql_query,
            "data": results,
            "row_count": len(results)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/execute-manual', methods=['POST'])
def execute_manual_query():
    """
    Execute a manually edited SQL query.
    Allows INSERT, UPDATE, DELETE operations for user-edited queries.
    
    Request Body:
        {
            "sql": "INSERT INTO employees (name, age, department, salary) VALUES ('John', 30, 'IT', 75000);"
        }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('sql'):
            return jsonify({
                "success": False,
                "error": "No SQL query provided"
            }), 400
        
        sql_query = data.get('sql', '').strip()
        
        if not sql_query:
            return jsonify({
                "success": False,
                "error": "Empty SQL query"
            }), 400
        
        # Basic security checks (prevent dangerous operations)
        dangerous_keywords = ['DROP', 'TRUNCATE', 'GRANT', 'REVOKE', 'ALTER', 'CREATE']
        sql_upper = sql_query.upper()
        
        for keyword in dangerous_keywords:
            if re.search(r'\b' + keyword + r'\b', sql_upper):
                return jsonify({
                    "success": False,
                    "error": f"Dangerous operation detected: {keyword}. Only SELECT, INSERT, UPDATE, DELETE are allowed.",
                    "sql": sql_query
                }), 400
        
        # Check for multiple statements
        if sql_query.count(';') > 1:
            return jsonify({
                "success": False,
                "error": "Multiple SQL statements not allowed",
                "sql": sql_query
            }), 400
        
        # Execute the query using the manual execution function
        success, results, message = execute_manual_sql(sql_query)
        
        if not success:
            return jsonify({
                "success": False,
                "error": message,
                "sql": sql_query
            }), 400
        
        return jsonify({
            "success": True,
            "sql": sql_query,
            "data": results,
            "affected_rows": len(results) if results else 0,
            "message": message
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# Error Handlers
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "success": False,
        "error": "Method not allowed"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# ============================================
# Application Entry Point
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Natural Language to SQL API Server")
    print("=" * 60)
    
    # Test database connection on startup
    db_connected, db_message = test_db_connection()
    print(f"📊 Database: {'✅ Connected' if db_connected else '❌ Not Connected'}")
    if not db_connected:
        print(f"   Message: {db_message}")
    
    # Check AI configuration
    ai_configured = (
        (ai_service.provider == 'openai' and ai_service.openai_key and ai_service.openai_key != 'your_openai_api_key_here') or
        (ai_service.provider == 'gemini' and ai_service.gemini_key and ai_service.gemini_key != 'your_gemini_api_key_here')
    )
    print(f"🤖 AI Service: {ai_service.provider.upper()} {'✅ Configured' if ai_configured else '⚠️ Not Configured'}")
    
    print("=" * 60)
    print("📡 API Endpoints:")
    print("   POST /api/prompt    - Convert NL to SQL and execute")
    print("   GET  /api/health    - Health check")
    print("   GET  /api/schema    - Get database schema")
    print("   GET  /api/examples  - Get example prompts")
    print("=" * 60)
    
    # Run the Flask development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )
