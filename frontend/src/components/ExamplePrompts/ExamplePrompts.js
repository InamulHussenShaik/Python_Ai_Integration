/**
 * ============================================
 * Example Prompts Component
 * ============================================
 * Clickable example prompts for quick testing
 */

import React, { useState } from 'react';
import './ExamplePrompts.css';

/**
 * ExamplePrompts component displaying clickable examples
 * 
 * @param {Object} props
 * @param {Array} props.examples - Array of example objects
 * @param {Function} props.onExampleClick - Click handler for examples
 */
function ExamplePrompts({ examples, onExampleClick }) {
    const [isExpanded, setIsExpanded] = useState(false);

    // Show first 4 examples by default, expand to show all
    const displayedExamples = isExpanded ? examples : examples.slice(0, 4);
    const hasMore = examples.length > 4;

    return (
        <div className="example-prompts">
            <div className="example-prompts__header">
                <h3 className="example-prompts__title">
                    <span className="example-prompts__icon">💡</span>
                    Try These Examples
                </h3>
            </div>

            <div className="example-prompts__list">
                {displayedExamples.map((example, index) => (
                    <button
                        key={index}
                        className="example-prompts__item"
                        onClick={() => onExampleClick(example.prompt)}
                        type="button"
                        title={example.description}
                    >
                        <span className="example-prompts__text">
                            "{example.prompt}"
                        </span>
                        <span className="example-prompts__arrow">→</span>
                    </button>
                ))}
            </div>

            {hasMore && (
                <button
                    className="example-prompts__toggle"
                    onClick={() => setIsExpanded(!isExpanded)}
                    type="button"
                >
                    {isExpanded ? (
                        <>
                            <span>Show Less</span>
                            <span className="toggle-icon">↑</span>
                        </>
                    ) : (
                        <>
                            <span>Show {examples.length - 4} More Examples</span>
                            <span className="toggle-icon">↓</span>
                        </>
                    )}
                </button>
            )}
        </div>
    );
}

export default ExamplePrompts;
