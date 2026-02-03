/**
 * ============================================
 * Header Component
 * ============================================
 * Application header with branding and status
 */

import React from 'react';
import './Header.css';

/**
 * Header component displaying app title and branding
 */
function Header() {
    return (
        <header className="header">
            <div className="header__container">
                {/* Logo and Title */}
                <div className="header__brand">
                    <div className="header__logo">
                        <span className="header__logo-icon">⚡</span>
                    </div>
                    <div className="header__text">
                        <h1 className="header__title">NL2SQL</h1>
                        <p className="header__tagline">Natural Language to SQL Generator</p>
                    </div>
                </div>

                {/* Tech Stack Badge */}
                <div className="header__badges">
                    <span className="header__badge header__badge--ai">
                        🤖 AI Powered
                    </span>
                    <span className="header__badge header__badge--tech">
                        MySQL + Flask + React
                    </span>
                </div>
            </div>
        </header>
    );
}

export default Header;
