/**
 * ============================================
 * SQL Display Component
 * ============================================
 * Read-only display of generated SQL query
 */

import React, { useState } from 'react';
import './SqlDisplay.css';

/**
 * SqlDisplay component for showing generated SQL
 * 
 * @param {Object} props
 * @param {string} props.sql - The SQL query to display
 */
function SqlDisplay({ sql }) {
    const [copied, setCopied] = useState(false);

    /**
     * Copy SQL to clipboard
     */
    const handleCopy = async () => {
        if (!sql) return;

        try {
            await navigator.clipboard.writeText(sql);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    };

    // Empty state
    if (!sql) {
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

    return (
        <div className="sql-display">
            {/* SQL Code Block */}
            <div className="sql-display__code-wrapper">
                <pre className="sql-display__code">
                    <code>{formatSql(sql)}</code>
                </pre>
            </div>

            {/* Actions */}
            <div className="sql-display__actions">
                <button
                    className={`sql-display__btn ${copied ? 'sql-display__btn--copied' : ''}`}
                    onClick={handleCopy}
                    type="button"
                    aria-label="Copy SQL to clipboard"
                >
                    {copied ? (
                        <>
                            <span className="btn-icon">✓</span>
                            <span>Copied!</span>
                        </>
                    ) : (
                        <>
                            <span className="btn-icon">📋</span>
                            <span>Copy SQL</span>
                        </>
                    )}
                </button>
            </div>
        </div>
    );
}

/**
 * Format SQL for better readability
 * Adds syntax highlighting-like formatting
 */
function formatSql(sql) {
    if (!sql) return '';

    // Basic formatting - uppercase keywords
    const keywords = [
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER',
        'ON', 'AS', 'ORDER', 'BY', 'GROUP', 'HAVING', 'LIMIT', 'OFFSET', 'ASC', 'DESC',
        'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'DISTINCT', 'IN', 'NOT', 'NULL', 'IS', 'LIKE',
        'BETWEEN', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'UNION', 'ALL', 'EXISTS'
    ];

    let formatted = sql;

    // This is a simple formatter - just ensure keywords are uppercase
    keywords.forEach(keyword => {
        const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
        formatted = formatted.replace(regex, keyword);
    });

    return formatted;
}

export default SqlDisplay;
