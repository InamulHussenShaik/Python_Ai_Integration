/**
 * ============================================
 * Data Table Component
 * ============================================
 * Displays query results in a styled table
 */

import React from 'react';
import './DataTable.css';

/**
 * DataTable component for displaying query results
 * 
 * @param {Object} props
 * @param {Array} props.data - Array of result objects
 * @param {boolean} props.isLoading - Loading state
 * @param {string} props.error - Error message if any
 */
function DataTable({ data, isLoading, error }) {
    // Loading state
    if (isLoading) {
        return (
            <div className="data-table__empty">
                <div className="data-table__loader">
                    <div className="loader-spinner"></div>
                    <p className="loader-text">Processing your query...</p>
                    <p className="loader-subtext">Converting to SQL and executing</p>
                </div>
            </div>
        );
    }

    // Error state
    if (error) {
        return (
            <div className="data-table__empty data-table__empty--error">
                <div className="data-table__icon">❌</div>
                <h4 className="data-table__message">Error</h4>
                <p className="data-table__error-text">{error}</p>
            </div>
        );
    }

    // Empty state - no data yet
    if (!data) {
        return (
            <div className="data-table__empty">
                <div className="data-table__icon">📊</div>
                <h4 className="data-table__message">No Data Yet</h4>
                <p className="data-table__hint">
                    Enter a natural language query to see results here
                </p>
            </div>
        );
    }

    // No results
    if (data.length === 0) {
        return (
            <div className="data-table__empty data-table__empty--warning">
                <div className="data-table__icon">🔍</div>
                <h4 className="data-table__message">No Results Found</h4>
                <p className="data-table__hint">
                    The query executed successfully but returned no matching records
                </p>
            </div>
        );
    }

    // Get column headers from the first row
    const columns = Object.keys(data[0]);

    return (
        <div className="data-table__container">
            <div className="data-table__wrapper">
                <table className="data-table">
                    <thead className="data-table__head">
                        <tr>
                            <th className="data-table__th data-table__th--index">#</th>
                            {columns.map((column, index) => (
                                <th key={index} className="data-table__th">
                                    {formatColumnName(column)}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody className="data-table__body">
                        {data.map((row, rowIndex) => (
                            <tr key={rowIndex} className="data-table__row">
                                <td className="data-table__td data-table__td--index">
                                    {rowIndex + 1}
                                </td>
                                {columns.map((column, colIndex) => (
                                    <td key={colIndex} className="data-table__td">
                                        {formatCellValue(row[column])}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

/**
 * Format column name for display
 * Converts snake_case to Title Case
 */
function formatColumnName(name) {
    return name
        .replace(/_/g, ' ')
        .replace(/\b\w/g, (char) => char.toUpperCase());
}

/**
 * Format cell value for display
 */
function formatCellValue(value) {
    if (value === null || value === undefined) {
        return <span className="data-table__null">NULL</span>;
    }

    if (typeof value === 'boolean') {
        return value ? '✓ Yes' : '✗ No';
    }

    if (typeof value === 'number') {
        // Format large numbers with commas
        if (Number.isInteger(value)) {
            return value.toLocaleString();
        }
        // Format decimal numbers (likely currency)
        return value.toLocaleString(undefined, {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    return String(value);
}

export default DataTable;
