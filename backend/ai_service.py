"""
============================================
AI Service Module for Natural Language to SQL
============================================
This module handles AI integration for converting natural language
prompts into SQL queries. Supports both OpenAI and Google Gemini.

Author: AI Integration Project
"""

import os
import re
import requests
from typing import Tuple, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIService:
    """
    AI Service for Natural Language to SQL conversion.
    Supports OpenAI GPT and Google Gemini models.
    """
    
    # Forbidden SQL operations for security
    FORBIDDEN_KEYWORDS = [
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
        'TRUNCATE', 'GRANT', 'REVOKE', 'EXECUTE', 'EXEC',
        'MERGE', 'CALL', 'LOAD', 'REPLACE', 'LOCK', 'UNLOCK'
    ]
    
    def __init__(self):
        """Initialize AI service with API keys and provider selection."""
        self.provider = os.getenv('AI_PROVIDER', 'gemini').lower()
        self.openai_key = os.getenv('OPENAI_API_KEY', '')
        self.gemini_key = os.getenv('GEMINI_API_KEY', '')
        
        # API endpoints
        self.openai_url = "https://api.openai.com/v1/chat/completions"
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
        print(f"✅ AI Service initialized with provider: {self.provider.upper()}")
    
    def get_system_prompt(self, schema_context: str) -> str:
        """
        Generate the system prompt for the AI model.
        
        Args:
            schema_context: Database schema description
            
        Returns:
            System prompt string
        """
        return f"""You are a MySQL query generator. Your ONLY job is to convert natural language requests into valid MySQL SELECT queries.

CRITICAL RULES:
1. Return ONLY the SQL query - no explanations, no markdown, no code blocks
2. Generate ONLY SELECT queries - never INSERT, UPDATE, DELETE, DROP, or any data-modifying operations
3. Use proper MySQL syntax
4. If the request cannot be converted to a SELECT query, return: ERROR: Cannot generate a valid SELECT query
5. Always use table and column names exactly as shown in the schema
6. Use appropriate JOINs when querying across multiple tables
7. Add appropriate WHERE clauses based on the natural language conditions
8. Use aliases for clarity when joining tables
9. End all queries with a semicolon

{schema_context}

IMPORTANT: Your response must contain ONLY the SQL query, nothing else. No explanations, no formatting, no markdown code blocks.

Examples of valid responses:
SELECT * FROM employees;
SELECT name, salary FROM employees WHERE age > 30;
SELECT e.name, d.name AS department FROM employees e JOIN departments d ON e.department_id = d.id;

Examples of INVALID responses:
```sql SELECT * FROM employees; ```
Here's the query: SELECT * FROM employees;
The SQL query would be: SELECT * FROM employees;"""
    
    def _call_openai(self, prompt: str, schema_context: str) -> Tuple[bool, str]:
        """
        Call OpenAI API to generate SQL.
        
        Args:
            prompt: User's natural language prompt
            schema_context: Database schema description
            
        Returns:
            Tuple of (success: bool, sql_or_error: str)
        """
        if not self.openai_key or self.openai_key == 'your_openai_api_key_here':
            return False, "OpenAI API key not configured"
        
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4",  # Can also use "gpt-3.5-turbo" for cost savings
            "messages": [
                {
                    "role": "system",
                    "content": self.get_system_prompt(schema_context)
                },
                {
                    "role": "user",
                    "content": f"Convert this to a MySQL SELECT query: {prompt}"
                }
            ],
            "temperature": 0.1,  # Low temperature for more deterministic output
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                self.openai_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                sql = data['choices'][0]['message']['content'].strip()
                return True, sql
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                return False, f"OpenAI API error: {error_msg}"
                
        except requests.exceptions.Timeout:
            return False, "OpenAI API request timed out"
        except requests.exceptions.RequestException as e:
            return False, f"OpenAI API request failed: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def _call_gemini(self, prompt: str, schema_context: str) -> Tuple[bool, str]:
        """
        Call Google Gemini API to generate SQL.
        
        Args:
            prompt: User's natural language prompt
            schema_context: Database schema description
            
        Returns:
            Tuple of (success: bool, sql_or_error: str)
        """
        if not self.gemini_key or self.gemini_key == 'your_gemini_api_key_here':
            return False, "Gemini API key not configured. Please add your GEMINI_API_KEY to the .env file."
        
        url = f"{self.gemini_url}?key={self.gemini_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Combine system prompt and user prompt for Gemini
        full_prompt = f"""{self.get_system_prompt(schema_context)}

User Request: {prompt}

SQL Query:"""
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 500,
                "topP": 0.8,
                "topK": 10
            }
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract text from Gemini response
                if 'candidates' in data and len(data['candidates']) > 0:
                    candidate = data['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        sql = candidate['content']['parts'][0]['text'].strip()
                        return True, sql
                
                return False, "No response generated by Gemini"
            else:
                error_msg = response.text
                return False, f"Gemini API error: {error_msg}"
                
        except requests.exceptions.Timeout:
            return False, "Gemini API request timed out"
        except requests.exceptions.RequestException as e:
            return False, f"Gemini API request failed: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def clean_sql_response(self, sql: str) -> str:
        """
        Clean the AI response to extract pure SQL.
        Removes markdown formatting, explanations, etc.
        
        Args:
            sql: Raw SQL response from AI
            
        Returns:
            Cleaned SQL query
        """
        # Remove markdown code blocks
        sql = re.sub(r'```sql\s*', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'```mysql\s*', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'```\s*', '', sql)
        
        # Remove common prefixes
        prefixes_to_remove = [
            "Here's the query:",
            "Here is the query:",
            "The SQL query is:",
            "SQL Query:",
            "Query:",
        ]
        for prefix in prefixes_to_remove:
            sql = re.sub(re.escape(prefix), '', sql, flags=re.IGNORECASE)
        
        # Remove leading/trailing whitespace and newlines
        sql = sql.strip()
        
        # Extract just the SQL statement if there's extra text
        # Look for SELECT statement
        select_match = re.search(r'(SELECT\s+.+?;)', sql, re.IGNORECASE | re.DOTALL)
        if select_match:
            sql = select_match.group(1)
        
        # Ensure query ends with semicolon
        if sql and not sql.endswith(';'):
            sql += ';'
        
        return sql
    
    def validate_sql(self, sql: str) -> Tuple[bool, str]:
        """
        Validate that the SQL is a safe SELECT query.
        
        Args:
            sql: SQL query to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not sql:
            return False, "Empty SQL query"
        
        # Check for ERROR response from AI
        if sql.upper().startswith('ERROR:'):
            return False, sql
        
        # Convert to uppercase for checking
        sql_upper = sql.upper()
        
        # Check that it starts with SELECT
        if not sql_upper.strip().startswith('SELECT'):
            return False, "Only SELECT queries are allowed"
        
        # Check for forbidden keywords
        for keyword in self.FORBIDDEN_KEYWORDS:
            # Use word boundary to avoid false positives
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                return False, f"Forbidden operation detected: {keyword}"
        
        # Check for multiple statements (SQL injection attempt)
        # Count semicolons (should be 0 or 1, at the end)
        semicolon_count = sql.count(';')
        if semicolon_count > 1:
            return False, "Multiple SQL statements not allowed"
        
        # Check for comment injection
        if '--' in sql or '/*' in sql:
            return False, "SQL comments not allowed"
        
        return True, "SQL query is valid"
    
    def generate_sql(self, prompt: str, schema_context: str) -> Tuple[bool, str, str]:
        """
        Main method to generate SQL from natural language.
        
        Args:
            prompt: User's natural language prompt
            schema_context: Database schema description
            
        Returns:
            Tuple of (success: bool, sql_or_error: str, message: str)
        """
        if not prompt or not prompt.strip():
            return False, "", "Empty prompt provided"
        
        # Call appropriate AI provider
        if self.provider == 'openai':
            success, result = self._call_openai(prompt, schema_context)
        else:
            success, result = self._call_gemini(prompt, schema_context)
        
        if not success:
            return False, "", result
        
        # Clean the SQL response
        sql = self.clean_sql_response(result)
        
        # Validate the SQL
        is_valid, validation_message = self.validate_sql(sql)
        
        if not is_valid:
            return False, sql, validation_message
        
        return True, sql, "SQL generated and validated successfully"


# Create a singleton instance for use across the application
ai_service = AIService()


# ============================================
# Module-level function for convenience
# ============================================

def convert_to_sql(prompt: str, schema_context: str) -> Tuple[bool, str, str]:
    """
    Convert natural language to SQL query.
    
    Args:
        prompt: Natural language prompt
        schema_context: Database schema description
        
    Returns:
        Tuple of (success: bool, sql: str, message: str)
    """
    return ai_service.generate_sql(prompt, schema_context)


# ============================================
# Test the module when run directly
# ============================================
if __name__ == "__main__":
    print("Testing AI Service Module...")
    print("=" * 50)
    
    # Sample schema context for testing
    sample_schema = """
Database Schema:

Table: employees
Columns:
  - id (int) [PRIMARY KEY]
  - name (varchar(50))
  - age (int)
  - department (varchar(50))
  - salary (decimal(10,2))

Table: departments
Columns:
  - id (int) [PRIMARY KEY]
  - name (varchar(100))
  - location (varchar(100))
"""
    
    # Test prompts
    test_prompts = [
        "Show all employees",
        "Find employees older than 30",
        "List employees with salary greater than 70000",
        "Get employees in the Engineering department"
    ]
    
    print(f"AI Provider: {ai_service.provider.upper()}")
    print(f"OpenAI Key configured: {'Yes' if ai_service.openai_key and ai_service.openai_key != 'your_openai_api_key_here' else 'No'}")
    print(f"Gemini Key configured: {'Yes' if ai_service.gemini_key and ai_service.gemini_key != 'your_gemini_api_key_here' else 'No'}")
    
    print("\n" + "=" * 50)
    print("Testing SQL Generation:")
    
    for prompt in test_prompts:
        print(f"\nPrompt: '{prompt}'")
        success, sql, message = convert_to_sql(prompt, sample_schema)
        if success:
            print(f"✅ Generated SQL: {sql}")
        else:
            print(f"❌ Failed: {message}")
            if sql:
                print(f"   Raw response: {sql}")
