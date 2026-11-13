// Contact page specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const messageInput = document.getElementById('message');
    
    // Real-time Form Validation
    if (nameInput) {
        nameInput.addEventListener('blur', function() {
            validateName(this);
        });
    }
    
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            validateEmail(this);
        });
    }
    
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            formatPhoneNumber(this);
        });
        phoneInput.addEventListener('blur', function() {
            validatePhone(this);
        });
    }
    
    if (messageInput) {
        messageInput.addEventListener('blur', function() {
            validateMessage(this);
        });
    }
    
    // Form Submission
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate all fields
            const isValid = validateForm();
            
            if (isValid) {
                // Show loading state
                const submitButton = this.querySelector('button[type="submit"]');
                const originalText = submitButton.textContent;
                submitButton.disabled = true;
                submitButton.textContent = 'Sending...';
                
                // Try WebSocket submission first, fallback to regular form
                if (window.WebSocketClient && window.WebSocketClient.isConnected()) {
                    const formData = {
                        name: nameInput.value,
                        email: emailInput.value,
                        phone: phoneInput.value,
                        project_type: document.getElementById('project_type').value,
                        location: document.getElementById('location').value,
                        budget_range: document.getElementById('budget_range').value,
                        message: messageInput.value
                    };
                    
                    if (window.WebSocketClient.submitContactForm(formData)) {
                        // Wait for WebSocket confirmation
                        setTimeout(() => {
                            submitButton.disabled = false;
                            submitButton.textContent = originalText;
                            contactForm.reset();
                        }, 1000);
                        return;
                    }
                }
                
                // Fallback to regular form submission
                this.submit();
            }
        });
    }
    
    // Validation Functions
    function validateName(input) {
        const value = input.value.trim();
        if (value.length < 2) {
            showError(input, 'Name must be at least 2 characters');
            return false;
        }
        hideError(input);
        return true;
    }
    
    function validateEmail(input) {
        const value = input.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showError(input, 'Please enter a valid email address');
            return false;
        }
        hideError(input);
        return true;
    }
    
    function validatePhone(input) {
        const value = input.value.replace(/\D/g, '');
        if (value.length < 10) {
            showError(input, 'Please enter a valid 10-digit phone number');
            return false;
        }
        hideError(input);
        return true;
    }
    
    function validateMessage(input) {
        const value = input.value.trim();
        if (value.length < 10) {
            showError(input, 'Message must be at least 10 characters');
            return false;
        }
        hideError(input);
        return true;
    }
    
    function validateForm() {
        let isValid = true;
        
        if (nameInput && !validateName(nameInput)) isValid = false;
        if (emailInput && !validateEmail(emailInput)) isValid = false;
        if (phoneInput && !validatePhone(phoneInput)) isValid = false;
        if (messageInput && !validateMessage(messageInput)) isValid = false;
        
        return isValid;
    }
    
    function showError(input, message) {
        hideError(input);
        input.classList.add('is-invalid');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        input.parentNode.appendChild(errorDiv);
    }
    
    function hideError(input) {
        input.classList.remove('is-invalid');
        const errorDiv = input.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    // Phone Number Formatting
    function formatPhoneNumber(input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length > 10) {
            value = value.substring(0, 10);
        }
        
        // Format as XXX-XXX-XXXX (optional)
        if (value.length > 6) {
            value = value.substring(0, 3) + '-' + value.substring(3, 6) + '-' + value.substring(6);
        } else if (value.length > 3) {
            value = value.substring(0, 3) + '-' + value.substring(3);
        }
        
        input.value = value;
    }
    
    // Email Validation
    function validateEmail(input) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(input.value.trim());
    }
    
    // Form Field Interactions
    const formFields = contactForm ? contactForm.querySelectorAll('input, textarea, select') : [];
    formFields.forEach(field => {
        field.addEventListener('focus', function() {
            this.parentNode.classList.add('focused');
        });
        
        field.addEventListener('blur', function() {
            this.parentNode.classList.remove('focused');
            if (this.value.trim()) {
                this.parentNode.classList.add('filled');
            } else {
                this.parentNode.classList.remove('filled');
            }
        });
    });
});

