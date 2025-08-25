// Campus Events Management System - Main JavaScript
// Professional interactions and enhancements

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeComponents();
    initializeFormValidation();
    initializeTooltips();
    initializeAnimations();

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            if (alert.querySelector('.btn-close')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);
});

// Initialize Bootstrap components
function initializeComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide loading spinners
    const spinners = document.querySelectorAll('.spinner-custom');
    spinners.forEach(function(spinner) {
        setTimeout(function() {
            spinner.style.display = 'none';
        }, 3000);
    });
}

// Form validation enhancements
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            // Add loading state to submit buttons
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;

                // Re-enable button after 10 seconds (fallback)
                setTimeout(function() {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 10000);
            }

            // Validate required fields
            const requiredFields = form.querySelectorAll('input[required], select[required], textarea[required]');
            let isValid = true;

            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                    field.classList.add('is-valid');
                }
            });

            // Email validation
            const emailFields = form.querySelectorAll('input[type="email"]');
            emailFields.forEach(function(field) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (field.value && !emailRegex.test(field.value)) {
                    field.classList.add('is-invalid');
                    showFieldError(field, 'Please enter a valid email address');
                    isValid = false;
                }
            });

            // Password confirmation validation
            const passwordField = form.querySelector('input[name="password"]');
            const confirmPasswordField = form.querySelector('input[name="confirm_password"]');

            if (passwordField && confirmPasswordField) {
                if (passwordField.value !== confirmPasswordField.value) {
                    confirmPasswordField.classList.add('is-invalid');
                    showFieldError(confirmPasswordField, 'Passwords do not match');
                    isValid = false;
                }
            }

            // Date validation for events
            const startDateField = form.querySelector('input[name="start_date"]');
            const endDateField = form.querySelector('input[name="end_date"]');

            if (startDateField && endDateField) {
                const startDate = new Date(startDateField.value);
                const endDate = new Date(endDateField.value);
                const now = new Date();

                if (startDate <= now) {
                    startDateField.classList.add('is-invalid');
                    showFieldError(startDateField, 'Start date must be in the future');
                    isValid = false;
                }

                if (endDate <= startDate) {
                    endDateField.classList.add('is-invalid');
                    showFieldError(endDateField, 'End date must be after start date');
                    isValid = false;
                }
            }

            if (!isValid) {
                event.preventDefault();
                // Re-enable submit button
                if (submitBtn) {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
                showNotification('Please fix the errors in the form', 'error');
            }
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(function(input) {
            input.addEventListener('blur', function() {
                validateField(input);
            });

            input.addEventListener('input', function() {
                if (input.classList.contains('is-invalid')) {
                    validateField(input);
                }
            });
        });
    });
}

// Field validation helper
function validateField(field) {
    const value = field.value.trim();
    let isValid = true;

    // Required field validation
    if (field.hasAttribute('required') && !value) {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
        showFieldError(field, 'This field is required');
        return false;
    }

    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
            showFieldError(field, 'Please enter a valid email address');
            return false;
        }
    }

    // Password strength validation
    if (field.type === 'password' && field.name === 'password' && value) {
        if (value.length < 8) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
            showFieldError(field, 'Password must be at least 8 characters long');
            return false;
        }
    }

    // If we get here, field is valid
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
    hideFieldError(field);
    return true;
}

// Show field error
function showFieldError(field, message) {
    let errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        field.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

// Hide field error
function hideFieldError(field) {
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Initialize tooltips
function initializeTooltips() {
    // Add tooltips to common elements
    const tooltipElements = [
        { selector: '.btn[disabled]', title: 'This action is not available' },
        { selector: '.badge', title: 'Status indicator' },
        { selector: '.fa-qrcode', title: 'QR Code for event check-in' },
        { selector: '.fa-star', title: 'Rating' },
        { selector: '.fa-users', title: 'Attendees' },
        { selector: '.fa-calendar', title: 'Event date' },
        { selector: '.fa-map-marker-alt', title: 'Event location' }
    ];

    tooltipElements.forEach(function(element) {
        const elements = document.querySelectorAll(element.selector);
        elements.forEach(function(el) {
            if (!el.hasAttribute('title') && !el.hasAttribute('data-bs-original-title')) {
                el.setAttribute('title', element.title);
                el.setAttribute('data-bs-toggle', 'tooltip');
                new bootstrap.Tooltip(el);
            }
        });
    });
}

// Initialize animations
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.animationDelay = (index * 0.1) + 's';
        card.classList.add('fade-in');
    });

    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Notification system
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';

    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // Auto-dismiss
    setTimeout(function() {
        if (notification.parentNode) {
            const bsAlert = new bootstrap.Alert(notification);
            bsAlert.close();
        }
    }, duration);
}

// Event search and filter functionality
function initializeEventSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    const categorySelect = document.querySelector('select[name="category"]');
    const dateSelect = document.querySelector('select[name="date"]');

    if (searchInput || categorySelect || dateSelect) {
        let searchTimeout;

        function performSearch() {
            const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
            const selectedCategory = categorySelect ? categorySelect.value : '';
            const selectedDate = dateSelect ? dateSelect.value : '';

            const eventCards = document.querySelectorAll('.event-card');

            eventCards.forEach(function(card) {
                const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
                const description = card.querySelector('.card-text')?.textContent.toLowerCase() || '';
                const category = card.querySelector('.badge')?.textContent || '';

                let showCard = true;

                // Search filter
                if (searchTerm && !title.includes(searchTerm) && !description.includes(searchTerm)) {
                    showCard = false;
                }

                // Category filter
                if (selectedCategory && category !== selectedCategory) {
                    showCard = false;
                }

                // Show/hide card
                if (showCard) {
                    card.style.display = 'block';
                    card.classList.add('fade-in');
                } else {
                    card.style.display = 'none';
                }
            });
        }

        // Debounced search
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(performSearch, 300);
            });
        }

        // Immediate filter on select change
        if (categorySelect) {
            categorySelect.addEventListener('change', performSearch);
        }

        if (dateSelect) {
            dateSelect.addEventListener('change', performSearch);
        }
    }
}

// File upload preview
function initializeFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file type
                const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
                if (!allowedTypes.includes(file.type)) {
                    showNotification('Please select a valid image file (JPEG, PNG, GIF)', 'error');
                    input.value = '';
                    return;
                }

                // Validate file size (max 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    showNotification('File size must be less than 5MB', 'error');
                    input.value = '';
                    return;
                }

                // Create preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = input.parentNode.querySelector('.file-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'file-preview mt-2';
                        input.parentNode.appendChild(preview);
                    }

                    preview.innerHTML = `
                        <img src="${e.target.result}" class="img-thumbnail" style="max-width: 200px; max-height: 150px;">
                        <p class="small text-muted mt-1">${file.name} (${(file.size / 1024).toFixed(1)} KB)</p>
                    `;
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

// Confirmation dialogs
function initializeConfirmDialogs() {
    const confirmButtons = document.querySelectorAll('[data-confirm]');

    confirmButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = button.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Delete confirmations
    const deleteButtons = document.querySelectorAll('button[onclick*="confirm"], form[action*="delete"] button[type="submit"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
}

// Auto-refresh for real-time updates
function initializeAutoRefresh() {
    // Only on dashboard pages
    if (window.location.pathname.includes('dashboard')) {
        // Refresh every 5 minutes
        setTimeout(function() {
            window.location.reload();
        }, 5 * 60 * 1000);
    }
}

// Print functionality
function printPage() {
    window.print();
}

// Export functionality
function exportData(data, filename, type = 'csv') {
    let content, mimeType;

    if (type === 'csv') {
        content = data;
        mimeType = 'text/csv';
    } else if (type === 'json') {
        content = JSON.stringify(data, null, 2);
        mimeType = 'application/json';
    }

    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    showNotification('Data exported successfully!', 'success');
}

// QR Code functionality
function generateQRCode(text, elementId) {
    const qrCodeDiv = document.getElementById(elementId);
    if (qrCodeDiv && typeof QRCode !== 'undefined') {
        qrCodeDiv.innerHTML = ''; // Clear existing QR code
        new QRCode(qrCodeDiv, {
            text: text,
            width: 128,
            height: 128,
            colorDark: "#000000",
            colorLight: "#ffffff"
        });
    }
}

// Copy to clipboard
function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showNotification(successMessage, 'success', 3000);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification(successMessage, 'success', 3000);
    }
}

// Utility functions
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(time) {
    return new Date(`2000-01-01T${time}`).toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize additional features when needed
function initializeAdditionalFeatures() {
    initializeEventSearch();
    initializeFileUpload();
    initializeConfirmDialogs();
    initializeAutoRefresh();
}

// Call additional features initialization
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initializeAdditionalFeatures, 500);
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showNotification('An unexpected error occurred. Please refresh the page.', 'error');
});

// Service worker registration (future enhancement)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.serviceWorker.register('/sw.js').then(function(registration) {
        //     console.log('SW registered: ', registration);
        // }).catch(function(registrationError) {
        //     console.log('SW registration failed: ', registrationError);
        // });
    });
}

// Export functions for global use
window.SMVEC = {
    showNotification,
    printPage,
    exportData,
    generateQRCode,
    copyToClipboard,
    formatDate,
    formatTime
};