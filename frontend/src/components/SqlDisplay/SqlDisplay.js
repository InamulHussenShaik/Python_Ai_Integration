/**
 * ============================================
 * SQL Display Component
 * ============================================
 * Simple display for generated SQL
 */

import React from 'react';
import './SqlDisplay.css';

/**
 * SqlDisplay component for showing and editing generated SQL
 * 
 * @param {Object} props
 * @param {string} props.sql - The SQL query to display
 * @param {boolean} props.isEditing - Whether in edit mode
 * @param {string} props.editedSql - The edited SQL value
 * @param {function} props.onEditedSqlChange - Callback when SQL is edited
 */
function SqlDisplay({ sql, isEditing, editedSql, onEditedSqlChange }) {
    // Empty state
    if (!sql && !isEditing) {
        return (
            <div className="sql-display sql-display--empty">
                <div className="sql-display__placeholder">
                    <span className="sql-display__placeholder-icon">⌨️</span>
                    <span className="sql-display__placeholder-text">
                        Generated SQL will appear here
                    </span>
                </div>
            </div>
        );
    }

    const displaySql = isEditing ? editedSql : sql;
    const isModified = editedSql !== sql;

    return (
        <div className="sql-display">
            {/* Header with mode indicator */}
            {isEditing && (
                <div className="sql-display__header">
                    <span className="sql-display__mode-badge">✏️ Editing Mode</span>
                    {isModified && (
                        <span className="sql-display__modified-badge">Modified</span>
                    )}
                </div>
            )}

            {/* SQL Code Block or Editor */}
            <div className="sql-display__code-wrapper">
                {isEditing ? (
                    <textarea
                        className="sql-display__editor"
                        value={editedSql}
                        onChange={(e) => onEditedSqlChange(e.target.value)}
                        placeholder="Enter your SQL query here..."
                        spellCheck={false}
                    />
                ) : (
                    <pre className="sql-display__code">
                        <code>{formatSql(displaySql)}</code>
                    </pre>
                )}
            </div>
        </div>
    );
}

/**
 * Format SQL for better readability
 */
function formatSql(sql) {
    if (!sql) return '';

    const keywords = [
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER',
        'ON', 'AS', 'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT', 'OFFSET', 'ASC', 'DESC',
        'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'DISTINCT', 'IN', 'NOT', 'NULL', 'IS', 'LIKE',
        'BETWEEN', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'UNION', 'ALL', 'EXISTS',
        'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE'
    ];

    let formatted = sql;

    keywords.forEach(keyword => {
        const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
        formatted = formatted.replace(regex, keyword);
    });

    return formatted;
}

export default SqlDisplay;
