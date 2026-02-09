/**
 * ============================================
 * API Service Module
 * ============================================
 * Handles all HTTP requests to the Flask backend
 */

// API Base URL - uses proxy in development
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

/**
 * Generic fetch wrapper with error handling
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Fetch options
 * @returns {Promise<Object>} - Response data
 */
async function fetchAPI(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, mergedOptions);

        // Parse JSON response
        const data = await response.json();

        // Handle HTTP errors
        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        // Network errors or JSON parsing errors
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error('Cannot connect to the server. Please ensure the backend is running.');
        }
        throw error;
    }
}

/**
 * Process a natural language prompt
 * Converts the prompt to SQL and executes it
 * 
 * @param {string} prompt - Natural language query
 * @returns {Promise<Object>} - Response with SQL and data
 * 
 * Response format:
 * {
 *   success: boolean,
 *   sql: string,
 *   data: Array<Object>,
 *   row_count: number,
 *   message: string
 * }
 */
export async function processPrompt(prompt) {
    return fetchAPI('/api/prompt', {
        method: 'POST',
        body: JSON.stringify({ prompt }),
    });
}

/**
 * Fetch example prompts from the API
 * 
 * @returns {Promise<Object>} - Response with examples array
 * 
 * Response format:
 * {
 *   success: boolean,
 *   examples: Array<{prompt: string, description: string}>
 * }
 */
export async function fetchExamples() {
    return fetchAPI('/api/examples', {
        method: 'GET',
    });
}

/**
 * Check API health status
 * 
 * @returns {Promise<Object>} - Health status
 * 
 * Response format:
 * {
 *   status: string,
 *   database: {connected: boolean, message: string},
 *   ai_service: {provider: string, configured: boolean}
 * }
 */
export async function checkHealth() {
    return fetchAPI('/api/health', {
        method: 'GET',
    });
}

/**
 * Get database schema information
 * 
 * @returns {Promise<Object>} - Schema information
 */
export async function getSchema() {
    return fetchAPI('/api/schema', {
        method: 'GET',
    });
}

/**
 * Execute a raw SQL query (for testing)
 * 
 * @param {string} sql - SQL query to execute
 * @returns {Promise<Object>} - Query results
 */
export async function executeRawQuery(sql) {
    return fetchAPI('/api/raw-query', {
        method: 'POST',
        body: JSON.stringify({ sql }),
    });
}

/**
 * Execute a manually edited SQL query
 * Supports SELECT, INSERT, UPDATE, DELETE operations
 * 
 * @param {string} sql - SQL query to execute
 * @returns {Promise<Object>} - Query results
 */
export async function executeManualQuery(sql) {
    return fetchAPI('/api/execute-manual', {
        method: 'POST',
        body: JSON.stringify({ sql }),
    });
}

// Export all functions
export default {
    processPrompt,
    fetchExamples,
    checkHealth,
    getSchema,
    executeRawQuery,
    executeManualQuery,
};
