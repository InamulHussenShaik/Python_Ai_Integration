/**
 * ============================================
 * Status Bar Component
 * ============================================
 * Bottom status bar showing API connection status
 */

import React from 'react';
import './StatusBar.css';

/**
 * StatusBar component displaying connection status
 * 
 * @param {Object} props
 * @param {Object} props.status - Status object with connection info
 */
function StatusBar({ status }) {
    return (
        <footer className="status-bar">
            <div className="status-bar__container">
                {/* Connection Status */}
                <div className="status-bar__item">
                    <span
                        className={`status-bar__indicator ${status.connected ? 'status-bar__indicator--success' : 'status-bar__indicator--error'
                            }`}
                    ></span>
                    <span className="status-bar__label">
                        API: {status.connected ? 'Connected' : 'Disconnected'}
                    </span>
                </div>

                {/* Database Status */}
                <div className="status-bar__item">
                    <span
                        className={`status-bar__indicator ${status.database ? 'status-bar__indicator--success' : 'status-bar__indicator--warning'
                            }`}
                    ></span>
                    <span className="status-bar__label">
                        Database: {status.database ? 'Connected' : 'Not Connected'}
                    </span>
                </div>

                {/* AI Status */}
                <div className="status-bar__item">
                    <span
                        className={`status-bar__indicator ${status.ai ? 'status-bar__indicator--success' : 'status-bar__indicator--warning'
                            }`}
                    ></span>
                    <span className="status-bar__label">
                        AI: {status.ai ? 'Ready' : 'Not Configured'}
                    </span>
                </div>

                {/* Spacer */}
                <div className="status-bar__spacer"></div>

                {/* Branding */}
                <div className="status-bar__brand">
                    <span>NL2SQL</span>
                    <span className="status-bar__version">v1.0</span>
                </div>
            </div>
        </footer>
    );
}

export default StatusBar;
