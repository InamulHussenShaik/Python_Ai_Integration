# Quick Start Guide - Enhanced Features

## Running the Application

### Backend (Terminal 1):
```bash
cd backend
.\venv\Scripts\activate
python app.py
```
**Runs on**: http://localhost:5000

### Frontend (Terminal 2):
```bash
cd frontend
npm start
```
**Runs on**: http://localhost:3000

## Using the Application

### 1. Natural Language Queries (Complex Multi-Table)

**Try these examples:**

✅ **Basic Query:**
```
"Show all employees"
```

✅ **Simple JOIN:**
```
"Show employees with their department names"
"List all employees and their departments"
```

✅ **Complex JOIN (3 tables):**
```
"Show employees, departments, and projects they work on"
"List employee names with their department and project details"
```

✅ **Aggregation:**
```
"Count how many employees are in each department"
"Show total salary by department"
```

✅ **Filtering with JOIN:**
```
"Find employees in Engineering with salary over 70000"
"Show projects worked on by employees older than 30"
```

### 2. Manual SQL Editing

**Step-by-step:**

1. **Enter a natural language query** → Click "Search"
2. **View the generated SQL** in "Generated Script" section
3. **Click "Edit SQL"** button
4. **Modify the SQL** (change to INSERT, UPDATE, DELETE)
5. **Click "Execute SQL"**
6. **View results** in the data table

**Example Edits:**

**Add a New Employee:**
```sql
INSERT INTO employees (name, age, department, salary, hire_date) 
VALUES ('Sarah Williams', 26, 'Sales', 65000, '2024-02-09');
```

**Update Salary:**
```sql
UPDATE employees 
SET salary = 95000 
WHERE name = 'John Doe';
```

**Delete Employee:**
```sql
DELETE FROM employees 
WHERE id = 5;
```

**Complex Update with JOIN:**
```sql
UPDATE employees e
JOIN departments d ON e.department_id = d.id
SET e.salary = e.salary * 1.1
WHERE d.name = 'Engineering';
```

## Quick Tips

✨ **For Complex Queries:**
- Be specific about which tables to join
- Mention the relationship (e.g., "employees in departments")
- Use natural language for conditions

✨ **For Manual Editing:**
- Always check the generated SQL first
- Use the Edit mode to safely modify queries
- Test with SELECT before running INSERT/UPDATE/DELETE
- Changes are immediate - be careful!

✨ **Security:**
- DROP, TRUNCATE, CREATE, ALTER are blocked
- Only one SQL statement at a time
- All modifications use transactions

## Common Workflows

### Workflow 1: Explore Data
```
1. "Show all employees" → See the data
2. "Show employees with departments" → Understand relationships
3. "Count employees by department" → Get insights
```

### Workflow 2: Add Data
```
1. "Show all employees" → Check current data
2. Edit SQL → Add INSERT statement
3. Execute → Add new record
4. "Show all employees" → Verify addition
```

### Workflow 3: Update Data
```
1. "Show employees in Engineering" → Find target records
2. Edit SQL → Change to UPDATE
3. Execute → Modify records
4. Run query again → Verify changes
```

### Workflow 4: Complex Analysis
```
1. "Show employees, departments, and projects" → Multi-table view
2. "Count projects per employee" → Aggregation
3. "Find employees working on multiple projects" → Complex filtering
```

## Keyboard Shortcuts

- **Enter** in prompt input → Submit query
- **Ctrl+A** in editor → Select all SQL
- **Esc** in editor → Cancel editing (future feature)

## Status Indicators

🟢 **Green Status Bar** = All systems operational
🔵 **Blue Badge** = Editing mode active
⚪ **Modified Badge** = SQL has been edited
🔴 **Red Error** = Query failed (check error message)

## Troubleshooting

**Backend not connecting?**
- Check if backend server is running on port 5000
- Look for "✅ Database connection pool created" message
- Verify .env file has correct credentials

**Frontend not loading?**
- Ensure npm start completed successfully
- Check browser console for errors
- Verify running on port 3000

**Query not working?**
- Check if table/column names are correct
- Review the database schema
- Try simpler queries first

**Manual SQL failing?**
- Verify SQL syntax is correct
- Ensure no dangerous operations (DROP, etc.)
- Check for proper WHERE clauses in UPDATE/DELETE

## Database Schema Reference

### Tables:
- `employees` - Employee information
- `departments` - Department details
- `projects` - Project information
- `employee_projects` - Many-to-many relationship

### Common Relationships:
- `employees.department_id` → `departments.id`
- `employee_projects.employee_id` → `employees.id`
- `employee_projects.project_id` → `projects.id`

## Support

For issues or questions:
1. Check the browser console for errors
2. Check backend terminal for error messages
3. Review FEATURES.md for detailed documentation
4. Check database connection in .env file
