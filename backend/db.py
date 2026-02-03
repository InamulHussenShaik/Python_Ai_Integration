"""
============================================
Database Connection and Operations Module
============================================
This module handles all database connections and query execution
for the Natural Language to SQL application.

Author: AI Integration Project
"""

import os
import mysql.connector
from mysql.connector import Error, pooling
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Tuple

# Load environment variables
load_dotenv()


class DatabaseManager:
    """
    Manages MySQL database connections and query execution.
    Uses connection pooling for better performance.
    """
    
    def __init__(self):
        """Initialize database configuration from environment variables."""
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'minematics'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'Inam@4a6'),
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'autocommit': True,
            'get_warnings': True,
            'raise_on_warnings': False
        }
        
        # Create connection pool for better performance
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="nl2sql_pool",
                pool_size=5,
                pool_reset_session=True,
                **self.config
            )
            print("✅ Database connection pool created successfully")
        except Error as e:
            print(f"❌ Error creating connection pool: {e}")
            self.pool = None
    
    def get_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """
        Get a connection from the pool.
        
        Returns:
            MySQL connection object or None if failed
        """
        try:
            if self.pool:
                return self.pool.get_connection()
            else:
                # Fallback to direct connection
                return mysql.connector.connect(**self.config)
        except Error as e:
            print(f"❌ Error getting connection: {e}")
            return None
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test the database connection.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        connection = None
        try:
            connection = self.get_connection()
            if connection and connection.is_connected():
                db_info = connection.get_server_info()
                cursor = connection.cursor()
                cursor.execute("SELECT DATABASE();")
                db_name = cursor.fetchone()[0]
                cursor.close()
                return True, f"Connected to MySQL Server version {db_info}, Database: {db_name}"
            return False, "Failed to establish connection"
        except Error as e:
            return False, f"Connection error: {str(e)}"
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    def execute_query(self, query: str) -> Tuple[bool, Any, str]:
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL SELECT query to execute
            
        Returns:
            Tuple of (success: bool, data: list/None, message: str)
        """
        connection = None
        cursor = None
        
        try:
            connection = self.get_connection()
            if not connection or not connection.is_connected():
                return False, None, "Failed to connect to database"
            
            # Use dictionary cursor for named column access
            cursor = connection.cursor(dictionary=True)
            
            # Execute the query
            cursor.execute(query)
            
            # Fetch all results
            results = cursor.fetchall()
            
            # Convert Decimal and datetime objects to JSON-serializable formats
            serializable_results = []
            for row in results:
                serializable_row = {}
                for key, value in row.items():
                    if hasattr(value, '__float__'):
                        # Handle Decimal types
                        serializable_row[key] = float(value)
                    elif hasattr(value, 'isoformat'):
                        # Handle datetime/date types
                        serializable_row[key] = value.isoformat()
                    else:
                        serializable_row[key] = value
                serializable_results.append(serializable_row)
            
            row_count = len(serializable_results)
            return True, serializable_results, f"Query executed successfully. {row_count} rows returned."
            
        except Error as e:
            error_message = f"Database error: {str(e)}"
            print(f"❌ {error_message}")
            return False, None, error_message
        
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    
    def get_table_schema(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Get the schema of all tables in the database.
        Useful for providing context to the AI model.
        
        Returns:
            Dictionary with table names as keys and column info as values
        """
        connection = None
        cursor = None
        schema = {}
        
        try:
            connection = self.get_connection()
            if not connection or not connection.is_connected():
                return schema
            
            cursor = connection.cursor(dictionary=True)
            
            # Get all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            # Get column info for each table
            for table_row in tables:
                table_name = list(table_row.values())[0]
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                schema[table_name] = [
                    {
                        'name': col['Field'],
                        'type': col['Type'],
                        'nullable': col['Null'] == 'YES',
                        'key': col['Key'],
                        'default': col['Default']
                    }
                    for col in columns
                ]
            
            return schema
            
        except Error as e:
            print(f"❌ Error getting schema: {e}")
            return schema
        
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
    
    def get_schema_description(self) -> str:
        """
        Get a human-readable description of the database schema.
        Used as context for the AI model.
        
        Returns:
            String description of the schema
        """
        schema = self.get_table_schema()
        
        if not schema:
            return "Unable to retrieve database schema."
        
        description_parts = ["Database Schema:\n"]
        
        for table_name, columns in schema.items():
            description_parts.append(f"\nTable: {table_name}")
            description_parts.append("Columns:")
            for col in columns:
                col_desc = f"  - {col['name']} ({col['type']})"
                if col['key'] == 'PRI':
                    col_desc += " [PRIMARY KEY]"
                elif col['key'] == 'MUL':
                    col_desc += " [FOREIGN KEY]"
                description_parts.append(col_desc)
        
        return "\n".join(description_parts)


# Create a singleton instance for use across the application
db_manager = DatabaseManager()


# ============================================
# Module-level functions for convenience
# ============================================

def test_db_connection() -> Tuple[bool, str]:
    """Test database connection."""
    return db_manager.test_connection()


def execute_sql(query: str) -> Tuple[bool, Any, str]:
    """Execute a SQL query."""
    return db_manager.execute_query(query)


def get_schema_context() -> str:
    """Get schema description for AI context."""
    return db_manager.get_schema_description()


# ============================================
# Test the module when run directly
# ============================================
if __name__ == "__main__":
    print("Testing Database Module...")
    print("=" * 50)
    
    # Test connection
    success, message = test_db_connection()
    print(f"Connection Test: {'✅ PASSED' if success else '❌ FAILED'}")
    print(f"Message: {message}")
    
    if success:
        print("\n" + "=" * 50)
        print("Database Schema:")
        print(get_schema_context())
        
        print("\n" + "=" * 50)
        print("Sample Query Test:")
        success, data, msg = execute_sql("SELECT * FROM employees LIMIT 3")
        if success:
            print(f"✅ Query returned {len(data)} rows")
            for row in data:
                print(f"  - {row}")
        else:
            print(f"❌ Query failed: {msg}")
