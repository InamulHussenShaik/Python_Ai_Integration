-- ============================================
-- Natural Language to SQL Project
-- Database: minematics
-- Author: AI Integration Project
-- ============================================

-- Create and use the database
CREATE DATABASE IF NOT EXISTS minematics;
USE minematics;

-- ============================================
-- TABLE 1: departments
-- Stores department information
-- ============================================
DROP TABLE IF EXISTS employee_projects;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100),
    budget DECIMAL(15, 2),
    manager_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================
-- TABLE 2: employees
-- Stores employee information (MANDATORY TABLE)
-- ============================================
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT CHECK (age >= 18 AND age <= 100),
    department VARCHAR(50),
    salary DECIMAL(10, 2),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    hire_date DATE,
    department_id INT,
    status ENUM('active', 'inactive', 'on_leave') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ============================================
-- TABLE 3: projects
-- Stores project information
-- ============================================
CREATE TABLE projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12, 2),
    status ENUM('planning', 'in_progress', 'completed', 'on_hold') DEFAULT 'planning',
    department_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ============================================
-- TABLE 4: employee_projects
-- Junction table for many-to-many relationship
-- ============================================
CREATE TABLE employee_projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL,
    project_id INT NOT NULL,
    role VARCHAR(50),
    hours_allocated INT DEFAULT 40,
    assigned_date DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE KEY unique_employee_project (employee_id, project_id)
) ENGINE=InnoDB;

-- ============================================
-- INSERT SAMPLE DATA
-- ============================================

-- Insert Departments
INSERT INTO departments (name, location, budget, manager_name) VALUES
('Engineering', 'Building A, Floor 3', 500000.00, 'Sarah Johnson'),
('Human Resources', 'Building B, Floor 1', 150000.00, 'Michael Chen'),
('Marketing', 'Building A, Floor 2', 300000.00, 'Emily Davis'),
('Finance', 'Building C, Floor 4', 250000.00, 'Robert Wilson'),
('Research & Development', 'Building D, Floor 5', 750000.00, 'Dr. Amanda Lee');

-- Insert Employees
INSERT INTO employees (name, age, department, salary, email, phone, hire_date, department_id, status) VALUES
('John Smith', 32, 'Engineering', 85000.00, 'john.smith@company.com', '+1-555-0101', '2020-03-15', 1, 'active'),
('Emily Johnson', 28, 'Engineering', 72000.00, 'emily.johnson@company.com', '+1-555-0102', '2021-06-20', 1, 'active'),
('Michael Brown', 45, 'Finance', 95000.00, 'michael.brown@company.com', '+1-555-0103', '2018-01-10', 4, 'active'),
('Sarah Williams', 35, 'Marketing', 68000.00, 'sarah.williams@company.com', '+1-555-0104', '2019-09-05', 3, 'active'),
('David Miller', 29, 'Engineering', 78000.00, 'david.miller@company.com', '+1-555-0105', '2022-02-28', 1, 'active'),
('Jessica Davis', 41, 'Human Resources', 62000.00, 'jessica.davis@company.com', '+1-555-0106', '2017-11-15', 2, 'active'),
('Christopher Wilson', 38, 'Research & Development', 105000.00, 'chris.wilson@company.com', '+1-555-0107', '2019-04-22', 5, 'active'),
('Amanda Taylor', 26, 'Marketing', 55000.00, 'amanda.taylor@company.com', '+1-555-0108', '2023-01-09', 3, 'active'),
('Daniel Anderson', 52, 'Finance', 110000.00, 'daniel.anderson@company.com', '+1-555-0109', '2015-07-30', 4, 'active'),
('Jennifer Thomas', 33, 'Engineering', 82000.00, 'jennifer.thomas@company.com', '+1-555-0110', '2020-10-12', 1, 'active'),
('Robert Martinez', 27, 'Research & Development', 88000.00, 'robert.martinez@company.com', '+1-555-0111', '2022-08-18', 5, 'active'),
('Lisa Garcia', 39, 'Human Resources', 67000.00, 'lisa.garcia@company.com', '+1-555-0112', '2018-05-25', 2, 'active'),
('James Robinson', 31, 'Engineering', 76000.00, 'james.robinson@company.com', '+1-555-0113', '2021-03-08', 1, 'on_leave'),
('Michelle Lee', 44, 'Marketing', 85000.00, 'michelle.lee@company.com', '+1-555-0114', '2016-12-01', 3, 'active'),
('Kevin White', 36, 'Research & Development', 98000.00, 'kevin.white@company.com', '+1-555-0115', '2019-08-14', 5, 'active'),
('Rachel Harris', 25, 'Finance', 52000.00, 'rachel.harris@company.com', '+1-555-0116', '2023-06-01', 4, 'active'),
('Steven Clark', 48, 'Engineering', 115000.00, 'steven.clark@company.com', '+1-555-0117', '2014-02-20', 1, 'active'),
('Karen Lewis', 30, 'Human Resources', 58000.00, 'karen.lewis@company.com', '+1-555-0118', '2022-04-11', 2, 'active'),
('Brian Walker', 42, 'Research & Development', 102000.00, 'brian.walker@company.com', '+1-555-0119', '2017-09-28', 5, 'active'),
('Nancy Hall', 34, 'Marketing', 71000.00, 'nancy.hall@company.com', '+1-555-0120', '2020-07-15', 3, 'inactive');

-- Insert Projects
INSERT INTO projects (name, description, start_date, end_date, budget, status, department_id) VALUES
('Cloud Migration', 'Migrate all legacy systems to cloud infrastructure', '2024-01-15', '2024-12-31', 200000.00, 'in_progress', 1),
('AI Platform', 'Develop internal AI tools for automation', '2024-03-01', '2025-06-30', 350000.00, 'in_progress', 5),
('Brand Refresh', 'Complete company rebranding initiative', '2024-02-01', '2024-08-31', 100000.00, 'completed', 3),
('Employee Portal', 'Build new employee self-service portal', '2024-04-15', '2024-11-30', 80000.00, 'in_progress', 2),
('Financial Analytics', 'Implement real-time financial dashboard', '2024-05-01', '2025-02-28', 150000.00, 'planning', 4),
('Mobile App', 'Develop company mobile application', '2024-06-01', '2025-03-31', 180000.00, 'in_progress', 1),
('Security Audit', 'Comprehensive security assessment', '2024-07-01', '2024-09-30', 50000.00, 'completed', 1),
('Market Research', 'Q3 market analysis and competitor research', '2024-07-15', '2024-10-15', 45000.00, 'in_progress', 3);

-- Insert Employee-Project Assignments
INSERT INTO employee_projects (employee_id, project_id, role, hours_allocated, assigned_date) VALUES
(1, 1, 'Tech Lead', 45, '2024-01-15'),
(2, 1, 'Developer', 40, '2024-01-20'),
(5, 1, 'Developer', 40, '2024-02-01'),
(10, 1, 'Developer', 35, '2024-02-15'),
(7, 2, 'Project Lead', 50, '2024-03-01'),
(11, 2, 'Researcher', 45, '2024-03-05'),
(15, 2, 'Developer', 40, '2024-03-10'),
(19, 2, 'Senior Developer', 45, '2024-03-15'),
(4, 3, 'Marketing Lead', 40, '2024-02-01'),
(8, 3, 'Designer', 35, '2024-02-10'),
(14, 3, 'Content Manager', 30, '2024-02-15'),
(6, 4, 'Project Manager', 45, '2024-04-15'),
(12, 4, 'HR Specialist', 40, '2024-04-20'),
(18, 4, 'Coordinator', 35, '2024-05-01'),
(3, 5, 'Finance Lead', 40, '2024-05-01'),
(9, 5, 'Senior Analyst', 45, '2024-05-05'),
(16, 5, 'Analyst', 35, '2024-05-10'),
(1, 6, 'Architect', 20, '2024-06-01'),
(5, 6, 'Developer', 40, '2024-06-05'),
(13, 6, 'Developer', 40, '2024-06-10'),
(17, 7, 'Security Lead', 50, '2024-07-01'),
(2, 7, 'Security Analyst', 30, '2024-07-05'),
(4, 8, 'Researcher', 25, '2024-07-15'),
(20, 8, 'Analyst', 35, '2024-07-20');

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Verify data insertion
SELECT 'Departments' AS table_name, COUNT(*) AS record_count FROM departments
UNION ALL
SELECT 'Employees', COUNT(*) FROM employees
UNION ALL
SELECT 'Projects', COUNT(*) FROM projects
UNION ALL
SELECT 'Employee_Projects', COUNT(*) FROM employee_projects;

-- Sample query to verify relationships
SELECT 
    e.name AS employee_name,
    e.department,
    e.salary,
    p.name AS project_name,
    ep.role
FROM employees e
JOIN employee_projects ep ON e.id = ep.employee_id
JOIN projects p ON ep.project_id = p.id
LIMIT 10;
