// Theme System - Dark/Light Mode & Color Themes

// Theme configuration
const themes = {
    light: {
        name: 'Light',
        icon: '☀️'
    },
    dark: {
        name: 'Dark',
        icon: '🌙'
    }
};

const colorThemes = {
    purple: {
        name: 'Purple',
        class: 'purple'
    },
    'black-white': {
        name: 'Black & White',
        class: 'black-white'
    },
    'neon-magenta-cyan': {
        name: 'Neon Magenta & Cyan',
        class: 'neon-magenta-cyan'
    },
    'orange-teal': {
        name: 'Orange & Teal',
        class: 'orange-teal'
    }
};

// Initialize theme from localStorage or default
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedColorTheme = localStorage.getItem('colorTheme') || 'purple';
    
    applyTheme(savedTheme, savedColorTheme);
    updateThemeUI(savedTheme, savedColorTheme);
}

// Apply theme to document
function applyTheme(theme, colorTheme) {
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.setAttribute('data-color-theme', colorTheme);
    document.documentElement.setAttribute('data-bs-theme', theme);
    
    // Update CSS variables
    updateCSSVariables(theme, colorTheme);
}

// Update CSS variables based on theme
function updateCSSVariables(theme, colorTheme) {
    const root = document.documentElement;
    
    // This is handled by CSS, but we can add custom logic here if needed
    console.log(`Theme applied: ${theme}, Color: ${colorTheme}`);
}

// Update theme UI elements
function updateThemeUI(theme, colorTheme) {
    // Update theme mode buttons
    document.querySelectorAll('.theme-mode-btn').forEach(btn => {
        if (btn.dataset.theme === theme) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Update color swatches
    document.querySelectorAll('.theme-color-item').forEach(item => {
        const swatch = item.querySelector('.theme-color-swatch');
        if (swatch && swatch.dataset.color === colorTheme) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Theme toggle button removed - using sidebar theme settings instead
}

// Toggle theme mode
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    const currentColorTheme = document.documentElement.getAttribute('data-color-theme') || 'purple';
    
    applyTheme(newTheme, currentColorTheme);
    updateThemeUI(newTheme, currentColorTheme);
    localStorage.setItem('theme', newTheme);
}

// Set color theme
function setColorTheme(colorTheme) {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    
    applyTheme(currentTheme, colorTheme);
    updateThemeUI(currentTheme, colorTheme);
    localStorage.setItem('colorTheme', colorTheme);
}

// Open theme modal
function openThemeModal() {
    const modal = document.getElementById('themeModal');
    if (modal) {
        modal.classList.add('active');
        // Update UI to show current settings
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const currentColorTheme = document.documentElement.getAttribute('data-color-theme') || 'purple';
        updateThemeUI(currentTheme, currentColorTheme);
    }
}

// Close theme modal
function closeThemeModal() {
    const modal = document.getElementById('themeModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    initTheme();
    
    // Theme toggle button
    // Theme toggle button removed - using sidebar theme settings instead
    
    // Theme modal open buttons (from navbar, sidebar, or anywhere)
    document.querySelectorAll('.theme-settings-trigger, #themeSettingsBtn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            openThemeModal();
        });
    });
    
    // Theme mode buttons
    document.querySelectorAll('.theme-mode-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const theme = this.dataset.theme;
            const currentColorTheme = document.documentElement.getAttribute('data-color-theme') || 'purple';
            applyTheme(theme, currentColorTheme);
            updateThemeUI(theme, currentColorTheme);
            localStorage.setItem('theme', theme);
        });
    });
    
    // Color theme swatches
    document.querySelectorAll('.theme-color-item').forEach(item => {
        item.addEventListener('click', function() {
            const swatch = this.querySelector('.theme-color-swatch');
            if (swatch) {
                const colorTheme = swatch.dataset.color;
                setColorTheme(colorTheme);
            }
        });
    });
    
    // Close modal buttons
    const closeModalBtn = document.getElementById('closeThemeModal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeThemeModal);
    }
    
    const doneBtn = document.getElementById('themeDoneBtn');
    if (doneBtn) {
        doneBtn.addEventListener('click', closeThemeModal);
    }
    
    // Close modal on outside click
    const modal = document.getElementById('themeModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeThemeModal();
            }
        });
    }
    
    // Keyboard shortcut: Ctrl/Cmd + Shift + T for theme toggle
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
            e.preventDefault();
            toggleTheme();
        }
    });
});

// Export functions for global use
window.ThemeManager = {
    toggleTheme: toggleTheme,
    setColorTheme: setColorTheme,
    openThemeModal: openThemeModal,
    closeThemeModal: closeThemeModal
};

