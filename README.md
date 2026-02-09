# Natural Language to SQL Query Generator

A complete end-to-end application that converts natural language prompts into SQL queries using AI, executes them on a MySQL database, and displays the results.

## 🏗️ Project Architecture

```
Python_Ai_Integration/
├── backend/                 # Flask REST API
│   ├── app.py              # Main Flask application
│   ├── db.py               # Database connection & operations
│   ├── ai_service.py       # AI integration for NL to SQL
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
├── frontend/               # React Application
│   ├── src/
│   │   ├── api/           # API service functions
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── App.js         # Main App component
│   │   └── App.css        # Global styles
│   ├── package.json
│   └── public/
├── database/
│   └── schema.sql         # Database schema & sample data
└── README.md
```

## 🚀 Features

- **Natural Language Processing**: Convert English prompts to SQL queries
- **Complex Multi-Table Queries**: Support for JOINs across 2, 3, or more tables with aggregations
- **AI-Powered**: Uses OpenAI GPT or Google Gemini for intelligent query generation
- **Manual SQL Editing**: Edit and execute queries directly, including INSERT, UPDATE, DELETE
- **Security First**: Dangerous operations (DROP, TRUNCATE, etc.) are blocked
- **Real-time Results**: Execute queries and display results instantly
- **Clean UI**: Modern React interface with split-panel design and editing mode
- **Transaction Support**: Data modifications use transactions with automatic rollback on errors

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- OpenAI API Key or Google Gemini API Key

## 🗃️ Database Setup

1. **Login to MySQL**:
   ```bash
   mysql -u root -p
   ```

2. **Run the schema script**:
   ```sql
   source database/schema.sql
   ```

   Or copy and paste the contents of `database/schema.sql` into your MySQL client.

## ⚙️ Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key
   # OPENAI_API_KEY=your_openai_api_key_here
   # OR
   # GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the Flask server**:
   ```bash
   python app.py
   ```
   
   Server runs on: `http://localhost:5000`

## 🎨 Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```
   
   App runs on: `http://localhost:3000`

## 📡 API Endpoints

### POST `/api/prompt`

Converts natural language to SQL and executes the query.

**Request Body**:
```json
{
  "prompt": "Show all employees older than 25"
}
```

**Response**:
```json
{
  "success": true,
  "sql": "SELECT * FROM employees WHERE age > 25;",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "age": 30,
      "department": "Engineering",
      "salary": 75000.00
    }
  ],
  "row_count": 1
}
```

### POST `/api/execute-manual`

Execute manually edited SQL queries (supports INSERT, UPDATE, DELETE).

**Request Body**:
```json
{
  "sql": "INSERT INTO employees (name, age, department, salary) VALUES ('Alice', 28, 'Sales', 65000);"
}
```

**Response**:
```json
{
  "success": true,
  "sql": "INSERT INTO employees (name, age, department, salary) VALUES ('Alice', 28, 'Sales', 65000);",
  "data": [],
  "affected_rows": 1,
  "message": "Successfully inserted 1 row(s)."
}
```

### GET `/api/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## 🔒 Security Features

1. **Dangerous Operation Blocking**: DROP, TRUNCATE, CREATE, ALTER, GRANT, REVOKE are blocked
2. **AI-Generated Query Validation**: AI-generated queries limited to SELECT only
3. **Manual Edit Safety**: Manual edits support SELECT, INSERT, UPDATE, DELETE only
4. **SQL Injection Prevention**: Multiple statements and comment injection blocked
5. **Transaction Support**: Data modifications use transactions with automatic rollback
6. **Environment Variables**: Sensitive data stored in `.env` files

## 📊 Database Schema

### Tables

1. **employees** - Main employee information
2. **departments** - Department details
3. **projects** - Project information
4. **employee_projects** - Many-to-many relationship

### Sample Queries

**Basic Queries:**
- "Show all employees"
- "Find employees with salary greater than 60000"
- "List employees in the Engineering department"
- "Show employees older than 30 sorted by salary"

**Multi-Table JOIN Queries:**
- "Show employees with their department names"
- "List employees and the projects they work on"
- "Get employees working on the AI Platform project"
- "Show all departments with their employee count"
- "Find employees in Engineering working on active projects"

**Complex Queries:**
- "Count how many employees are in each department"
- "Show total salary by department"
- "List employees, departments, and all their projects"
- "Find departments with more than 5 employees"
- "Show employees with salary above department average"

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, CSS3 |
| Backend | Python 3, Flask |
| Database | MySQL 8.0 |
| AI | OpenAI GPT-4 / Google Gemini |

## 📝 License

MIT License - feel free to use this project for learning and development.

## � Documentation

- **[FEATURES.md](FEATURES.md)** - Detailed guide on complex queries and manual SQL editing
- **[QUICK_START.md](QUICK_START.md)** - Quick reference for common tasks and workflows

## 💡 New Features

### Complex Multi-Table Queries
Ask questions that span multiple tables! Examples:
- "Show employees with their department names"
- "List employees, departments, and projects they work on"
- "Count employees in each department"

### Manual SQL Editing
Edit and execute queries directly:
1. Generate a query with natural language
2. Click "Edit SQL" to modify the query
3. Change to INSERT, UPDATE, or DELETE as needed
4. Execute directly from the interface

See [FEATURES.md](FEATURES.md) for complete documentation.

## �👤 Author

Built with ❤️ for interview preparation and learning purposes.
