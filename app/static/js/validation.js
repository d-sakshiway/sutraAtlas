/**
 * Client-side validation utilities for SutraAtlas
 * Provides robust form validation and URL protection
 */

// Validation patterns
const VALIDATION_PATTERNS = {
    email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    username: /^[a-zA-Z0-9_-]+$/,
    url: /^https?:\/\/.+/i
};

// Field length limits (matching backend)
const FIELD_LIMITS = {
    email: { max: 254 },
    username: { min: 3, max: 50 },
    password: { min: 8, max: 128 },
    title: { min: 1, max: 300 },
    description: { max: 1000 },
    authors: { max: 500 },
    url: { max: 1000 }
};

/**
 * Validates an email address
 * @param {string} email - Email to validate
 * @returns {object} - {valid: boolean, error: string}
 */
function validateEmail(email) {
    if (!email || email.trim() === '') {
        return { valid: false, error: 'Email is required' };
    }
    
    email = email.trim().toLowerCase();
    
    if (email.length > FIELD_LIMITS.email.max) {
        return { valid: false, error: 'Email too long' };
    }
    
    if (!VALIDATION_PATTERNS.email.test(email)) {
        return { valid: false, error: 'Invalid email format' };
    }
    
    return { valid: true, value: email };
}

/**
 * Validates a username
 * @param {string} username - Username to validate
 * @param {boolean} required - Whether username is required
 * @returns {object} - {valid: boolean, error: string}
 */
function validateUsername(username, required = false) {
    if (!username || username.trim() === '') {
        if (required) {
            return { valid: false, error: 'Username is required' };
        }
        return { valid: true, value: '' };
    }
    
    username = username.trim();
    
    if (username.length < FIELD_LIMITS.username.min) {
        return { valid: false, error: `Username must be at least ${FIELD_LIMITS.username.min} characters` };
    }
    
    if (username.length > FIELD_LIMITS.username.max) {
        return { valid: false, error: `Username too long (max ${FIELD_LIMITS.username.max} characters)` };
    }
    
    if (!VALIDATION_PATTERNS.username.test(username)) {
        return { valid: false, error: 'Username can only contain letters, numbers, hyphens, and underscores' };
    }
    
    return { valid: true, value: username };
}

/**
 * Validates a password
 * @param {string} password - Password to validate
 * @returns {object} - {valid: boolean, error: string}
 */
function validatePassword(password) {
    if (!password) {
        return { valid: false, error: 'Password is required' };
    }
    
    if (password.length < FIELD_LIMITS.password.min) {
        return { valid: false, error: `Password must be at least ${FIELD_LIMITS.password.min} characters` };
    }
    
    if (password.length > FIELD_LIMITS.password.max) {
        return { valid: false, error: `Password too long (max ${FIELD_LIMITS.password.max} characters)` };
    }
    
    if (!/[A-Z]/.test(password)) {
        return { valid: false, error: 'Password must contain at least one uppercase letter' };
    }
    
    if (!/[a-z]/.test(password)) {
        return { valid: false, error: 'Password must contain at least one lowercase letter' };
    }
    
    if (!/[0-9]/.test(password)) {
        return { valid: false, error: 'Password must contain at least one number' };
    }
    
    return { valid: true };
}

/**
 * Validates a title field
 * @param {string} title - Title to validate
 * @returns {object} - {valid: boolean, error: string}
 */
function validateTitle(title) {
    if (!title || title.trim() === '') {
        return { valid: false, error: 'Title is required' };
    }
    
    title = title.trim();
    
    if (title.length > FIELD_LIMITS.title.max) {
        return { valid: false, error: `Title too long (max ${FIELD_LIMITS.title.max} characters)` };
    }
    
    return { valid: true, value: title };
}

/**
 * Validates a description field
 * @param {string} description - Description to validate
 * @param {boolean} required - Whether description is required
 * @returns {object} - {valid: boolean, error: string}
 */
function validateDescription(description, required = false) {
    if (!description || description.trim() === '') {
        if (required) {
            return { valid: false, error: 'Description is required' };
        }
        return { valid: true, value: '' };
    }
    
    description = description.trim();
    
    if (description.length > FIELD_LIMITS.description.max) {
        return { valid: false, error: `Description too long (max ${FIELD_LIMITS.description.max} characters)` };
    }
    
    return { valid: true, value: description };
}

/**
 * Validates an authors field
 * @param {string} authors - Authors to validate
 * @returns {object} - {valid: boolean, error: string}
 */
function validateAuthors(authors) {
    if (!authors || authors.trim() === '') {
        return { valid: true, value: '' };
    }
    
    authors = authors.trim();
    
    if (authors.length > FIELD_LIMITS.authors.max) {
        return { valid: false, error: `Authors field too long (max ${FIELD_LIMITS.authors.max} characters)` };
    }
    
    return { valid: true, value: authors };
}

/**
 * Validates a URL field
 * @param {string} url - URL to validate
 * @returns {object} - {valid: boolean, error: string}
 */
function validateUrl(url) {
    if (!url || url.trim() === '') {
        return { valid: true, value: '' };
    }
    
    url = url.trim();
    
    if (url.length > FIELD_LIMITS.url.max) {
        return { valid: false, error: `URL too long (max ${FIELD_LIMITS.url.max} characters)` };
    }
    
    // Auto-fix common URL issues
    if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
        url = 'https://' + url;
    }
    
    if (url && !VALIDATION_PATTERNS.url.test(url)) {
        return { valid: false, error: 'Invalid URL format' };
    }
    
    return { valid: true, value: url };
}

/**
 * Validates that two passwords match
 * @param {string} password1 - First password
 * @param {string} password2 - Second password
 * @returns {object} - {valid: boolean, error: string}
 */
function validatePasswordMatch(password1, password2) {
    if (password1 !== password2) {
        return { valid: false, error: 'Passwords do not match' };
    }
    return { valid: true };
}

/**
 * Shows validation error for a field
 * @param {string} fieldName - Name of the field
 * @param {string} error - Error message
 */
function showFieldError(fieldName, error) {
    const field = document.getElementById(fieldName);
    const errorElement = document.getElementById(`${fieldName}-error`);
    
    if (field) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
    }
    
    if (errorElement) {
        errorElement.textContent = error;
        errorElement.style.display = 'block';
    } else {
        // Create error element if it doesn't exist
        const newErrorElement = document.createElement('div');
        newErrorElement.id = `${fieldName}-error`;
        newErrorElement.className = 'invalid-feedback d-block';
        newErrorElement.textContent = error;
        
        if (field && field.parentNode) {
            field.parentNode.insertBefore(newErrorElement, field.nextSibling);
        }
    }
}

/**
 * Clears validation error for a field
 * @param {string} fieldName - Name of the field
 */
function clearFieldError(fieldName) {
    const field = document.getElementById(fieldName);
    const errorElement = document.getElementById(`${fieldName}-error`);
    
    if (field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    }
    
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

/**
 * Clears all validation errors from a form
 * @param {HTMLFormElement} form - Form element
 */
function clearAllErrors(form) {
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.classList.remove('is-invalid', 'is-valid');
    });
    
    const errorElements = form.querySelectorAll('.invalid-feedback');
    errorElements.forEach(element => {
        element.style.display = 'none';
    });
}

/**
 * Prevents URL manipulation by validating route parameters
 * @param {string} type - Type of entity (collection, resource)
 * @param {string} id - ID parameter from URL
 * @returns {boolean} - Whether ID is valid
 */
function validateUrlParameter(type, id) {
    if (!id || isNaN(parseInt(id)) || parseInt(id) <= 0) {
        console.error(`Invalid ${type} ID in URL: ${id}`);
        showAlert('error', `Invalid ${type} ID. Redirecting to ${type}s page.`);
        
        // Redirect to safe page after short delay
        setTimeout(() => {
            if (type === 'collection') {
                window.location.href = '/collections';
            } else if (type === 'resource') {
                window.location.href = '/collections';
            }
        }, 2000);
        
        return false;
    }
    return true;
}

/**
 * Checks if user is authenticated by making a request to /api/auth/me
 * @returns {Promise<boolean>} - Whether user is authenticated
 */
async function checkAuthentication() {
    try {
        const response = await fetch('/api/auth/me', {
            credentials: 'include',
            method: 'GET'
        });
        return response.ok;
    } catch (error) {
        console.error('Authentication check failed:', error);
        return false;
    }
}

/**
 * Redirects to login page if user is not authenticated
 * @param {string} redirectMessage - Custom message to show on login page
 */
async function requireAuthentication(redirectMessage = 'Please log in to access this page.') {
    const isAuthenticated = await checkAuthentication();
    
    if (!isAuthenticated) {
        // Store the intended destination
        sessionStorage.setItem('intendedDestination', window.location.pathname);
        
        // Show message and redirect
        showAlert('info', redirectMessage + ' Redirecting to login...');
        
        setTimeout(() => {
            window.location.href = '/login';
        }, 1500);
        
        return false;
    }
    
    return true;
}

/**
 * Shows an alert message
 * @param {string} type - Alert type (success, error, warning, info)
 * @param {string} message - Alert message
 */
function showAlert(type, message) {
    const alertContainer = document.getElementById('alert-container') || document.body;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

/**
 * Protects against CSRF by ensuring requests have proper tokens
 * @param {string} token - CSRF token
 * @returns {boolean} - Whether token is valid
 */
function validateCSRFToken(token) {
    if (!token || token.length < 10) {
        console.error('Missing or invalid CSRF token');
        showAlert('error', 'Security token missing. Please refresh the page.');
        return false;
    }
    return true;
}

// Initialize validation on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add real-time validation to all forms
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            // Add real-time validation on blur
            input.addEventListener('blur', function() {
                const fieldName = this.name || this.id;
                const value = this.value;
                
                let validation = { valid: true };
                
                switch (fieldName) {
                    case 'email':
                        validation = validateEmail(value);
                        break;
                    case 'username':
                        validation = validateUsername(value);
                        break;
                    case 'password':
                        validation = validatePassword(value);
                        break;
                    case 'title':
                        validation = validateTitle(value);
                        break;
                    case 'description':
                        validation = validateDescription(value);
                        break;
                    case 'authors':
                        validation = validateAuthors(value);
                        break;
                    case 'url':
                        validation = validateUrl(value);
                        if (validation.valid && validation.value !== undefined) {
                            this.value = validation.value; // Auto-fix URL
                        }
                        break;
                }
                
                if (validation.valid) {
                    clearFieldError(fieldName);
                } else {
                    showFieldError(fieldName, validation.error);
                }
            });
            
            // Clear error on focus
            input.addEventListener('focus', function() {
                const fieldName = this.name || this.id;
                clearFieldError(fieldName);
            });
        });
    });
    
    // Validate URL parameters on pages with IDs
    const currentPath = window.location.pathname;
    const pathParts = currentPath.split('/');
    
    // Check for collection or resource IDs in URL
    if (pathParts.includes('collection') && pathParts.length > 2) {
        const collectionId = pathParts[pathParts.indexOf('collection') + 1];
        validateUrlParameter('collection', collectionId);
    }
    
    if (pathParts.includes('resource') && pathParts.length > 2) {
        const resourceId = pathParts[pathParts.indexOf('resource') + 1];
        validateUrlParameter('resource', resourceId);
    }
});

// Export validation functions for global use
window.SutraValidation = {
    validateEmail,
    validateUsername,
    validatePassword,
    validateTitle,
    validateDescription,
    validateAuthors,
    validateUrl,
    validatePasswordMatch,
    showFieldError,
    clearFieldError,
    clearAllErrors,
    validateUrlParameter,
    showAlert,
    validateCSRFToken,
    checkAuthentication,
    requireAuthentication
};