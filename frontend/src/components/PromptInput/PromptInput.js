/**
 * ============================================
 * Prompt Input Component
 * ============================================
 * Text input area for natural language queries
 */

import React, { useRef, useEffect } from 'react';
import './PromptInput.css';

/**
 * PromptInput component with textarea and action buttons
 * 
 * @param {Object} props
 * @param {string} props.value - Current input value
 * @param {Function} props.onChange - Value change handler
 * @param {Function} props.onSubmit - Submit handler
 * @param {Function} props.onClear - Clear handler
 * @param {boolean} props.isLoading - Loading state
 * @param {boolean} props.disabled - Disabled state
 */
function PromptInput({ value, onChange, onSubmit, onClear, isLoading, disabled }) {
    const textareaRef = useRef(null);

    // Focus on mount
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.focus();
        }
    }, []);

    // Handle keyboard shortcuts
    const handleKeyDown = (e) => {
        // Ctrl/Cmd + Enter to submit
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!isLoading && !disabled && value.trim()) {
                onSubmit();
            }
        }
        // Escape to clear
        if (e.key === 'Escape') {
            onClear();
        }
    };

    return (
        <div className="prompt-input">
            {/* Textarea */}
            <div className="prompt-input__wrapper">
                <textarea
                    ref={textareaRef}
                    className="prompt-input__textarea"
                    placeholder="Ask a question about your data...&#10;&#10;Example: Show all employees older than 30"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={disabled || isLoading}
                    rows={5}
                    aria-label="Natural language query input"
                />

                {/* Character count */}
                <div className="prompt-input__count">
                    {value.length} characters
                </div>
            </div>

            {/* Action Buttons */}
            <div className="prompt-input__actions">
                <button
                    className="prompt-input__btn prompt-input__btn--clear"
                    onClick={onClear}
                    disabled={!value || isLoading}
                    type="button"
                    aria-label="Clear input"
                >
                    <span className="btn-icon">✕</span>
                    <span className="btn-text">Clear</span>
                </button>

                <button
                    className="prompt-input__btn prompt-input__btn--submit"
                    onClick={onSubmit}
                    disabled={!value.trim() || isLoading || disabled}
                    type="button"
                    aria-label="Submit query"
                >
                    {isLoading ? (
                        <>
                            <span className="btn-spinner"></span>
                            <span className="btn-text">Processing...</span>
                        </>
                    ) : (
                        <>
                            <span className="btn-icon">▶</span>
                            <span className="btn-text">Generate Data & Script</span>
                        </>
                    )}
                </button>
            </div>

            {/* Keyboard Shortcuts Hint */}
            <p className="prompt-input__hint">
                <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to submit • <kbd>Esc</kbd> to clear
            </p>
        </div>
    );
}

export default PromptInput;
