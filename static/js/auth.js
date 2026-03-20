/**
 * Authentication utilities for JWT-based authentication
 * Handles token management, storage, and API communication
 */

/**
 * Store authentication token and user data
 */
function storeAuthData(token, user) {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
}

/**
 * Retrieve stored token
 */
function getToken() {
    return localStorage.getItem('token');
}

/**
 * Retrieve stored user data
 */
function getUser() {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
    return !!getToken();
}

/**
 * Clear authentication data
 */
function clearAuthData() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
}

/**
 * Make authenticated API request
 */
async function makeAuthenticatedRequest(url, options = {}) {
    const token = getToken();
    
    if (!token) {
        throw new Error('No authentication token found');
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };

    const response = await fetch(url, {
        ...options,
        headers
    });

    return response;
}

/**
 * Verify token is still valid by calling protected endpoint
 */
async function verifyToken(token) {
    try {
        const response = await fetch('/api/profile', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        return response.ok;
    } catch (error) {
        return false;
    }
}

/**
 * Setup authentication UI based on login state
 */
function setupAuthUI() {
    const token = getToken();
    const user = getUser();
    const loginLink = document.getElementById('loginLink');
    const registerLink = document.getElementById('registerLink');
    const profileLink = document.getElementById('profileLink');
    const logoutBtn = document.getElementById('logoutBtn');

    if (token && user) {
        if (loginLink) loginLink.style.display = 'none';
        if (registerLink) registerLink.style.display = 'none';
        if (profileLink) profileLink.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (registerLink) registerLink.style.display = 'block';
        if (profileLink) profileLink.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'none';
    }
}

/**
 * Format date string to readable format
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Initialize auth UI on page load
document.addEventListener('DOMContentLoaded', setupAuthUI);
