// WebSocket functionality for real-time features

// Initialize Socket.IO connection with websocket priority
const socket = io({ transports: ['websocket', 'polling'], timeout: 5000 });

// Connection status
let isConnected = false;

// Connect event
socket.on('connect', function() {
    isConnected = true;
    console.log('Connected to server via WebSocket');
    
    // Join general room
    socket.emit('join_room', { room: 'general' });
    
    // Show connection indicator
    showConnectionStatus(true);
});

// Disconnect event
socket.on('disconnect', function() {
    isConnected = false;
    console.log('Disconnected from server');
    showConnectionStatus(false);
});

// Connected confirmation
socket.on('connected', function(data) {
    console.log('Server confirmation:', data.message);
});

// Joined room confirmation
socket.on('joined_room', function(data) {
    console.log('Joined room:', data.room);
});

// New message (for chat)
socket.on('new_message', function(data) {
    displayMessage(data);
});

// Form submission confirmation
socket.on('form_submitted', function(data) {
    if (data.success) {
        showNotification(data.message, 'success');
    }
});

// Quote request confirmation
socket.on('quote_requested', function(data) {
    if (data.success) {
        showNotification(data.message, 'success');
    }
});

// User typing indicator
socket.on('user_typing', function(data) {
    showTypingIndicator(data.username, data.typing);
});

// New lead notification (for admin)
socket.on('new_lead', function(data) {
    showAdminNotification('New Lead', `${data.name} submitted a contact form`, 'info');
});

// New quote request notification (for admin)
socket.on('new_quote_request', function(data) {
    showAdminNotification('New Quote Request', `${data.project_type} project in ${data.location}`, 'warning');
});

// Project viewed notification (for admin)
socket.on('project_viewed', function(data) {
    // Track analytics
    console.log('Project viewed:', data.project_id);
});

// Real-time Contact Form Submission
function submitContactFormWebSocket(formData) {
    if (!isConnected) {
        console.warn('WebSocket not connected, using regular form submission');
        return false;
    }
    
    socket.emit('contact_form_submit', {
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        project_type: formData.project_type,
        location: formData.location,
        budget_range: formData.budget_range,
        message: formData.message
    });
    
    return true;
}

// Real-time Quote Request
function requestQuoteWebSocket(projectType, location) {
    if (!isConnected) {
        return false;
    }
    
    socket.emit('request_quote', {
        project_type: projectType,
        location: location
    });
    
    return true;
}

// Track Project Views
function trackProjectView(projectId) {
    if (isConnected && projectId) {
        socket.emit('project_view', {
            project_id: projectId
        });
    }
}

// Chat Functions
function sendChatMessage(message, username, room = 'general') {
    if (!isConnected) {
        console.warn('WebSocket not connected');
        return false;
    }
    
    socket.emit('send_message', {
        message: message,
        username: username || 'Guest',
        room: room
    });
    
    return true;
}

// Typing Indicator
let typingTimeout;
function sendTypingIndicator(username, isTyping, room = 'general') {
    if (!isConnected) return;
    
    clearTimeout(typingTimeout);
    
    socket.emit('typing', {
        username: username || 'Guest',
        typing: isTyping,
        room: room
    });
    
    if (isTyping) {
        typingTimeout = setTimeout(() => {
            socket.emit('typing', {
                username: username || 'Guest',
                typing: false,
                room: room
            });
        }, 3000);
    }
}

// Notification Subscription
function subscribeToNotifications(userId) {
    if (isConnected) {
        socket.emit('notification_subscribe', {
            user_id: userId
        });
    }
}

// Display Functions
function displayMessage(data) {
    const chatContainer = document.getElementById('chatMessages');
    if (chatContainer) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message mb-2';
        messageDiv.innerHTML = `
            <strong>${data.username}:</strong> ${data.message}
            <small class="text-muted ms-2">${data.timestamp}</small>
        `;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

function showConnectionStatus(connected) {
    // Connection status indicator removed
    // Status can be logged to console if needed
    if (connected) {
        console.log('WebSocket: Connected');
    } else {
        console.log('WebSocket: Disconnected');
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function showAdminNotification(title, message, type = 'info') {
    // Only show if user is admin (you can add admin check)
    console.log(`[${title}] ${message}`);
    showNotification(`${title}: ${message}`, type);
}

function showTypingIndicator(username, isTyping) {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        if (isTyping) {
            typingIndicator.textContent = `${username} is typing...`;
            typingIndicator.style.display = 'block';
        } else {
            typingIndicator.style.display = 'none';
        }
    }
}

// Export functions for use in other scripts
window.WebSocketClient = {
    isConnected: () => isConnected,
    submitContactForm: submitContactFormWebSocket,
    requestQuote: requestQuoteWebSocket,
    trackProjectView: trackProjectView,
    sendChatMessage: sendChatMessage,
    sendTypingIndicator: sendTypingIndicator,
    subscribeToNotifications: subscribeToNotifications
};

