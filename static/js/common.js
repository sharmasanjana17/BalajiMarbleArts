// Common JavaScript for all pages

// Initialize WebSocket (if websocket.js is loaded)
if (typeof socket !== 'undefined') {
    // WebSocket is available
    console.log('WebSocket support enabled');
}

// Navigation Toggle (Mobile)
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.navbar') && navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        }
    });
});

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Instant Navigation: Prefetch HTML on hover/touch before click
(function() {
    const prefetched = new Set();
    function prefetch(url) {
        if (!url || prefetched.has(url)) return;
        try {
            const u = new URL(url, window.location.origin);
            if (u.origin === window.location.origin && !u.pathname.startsWith('/admin') && !u.pathname.startsWith('/static')) {
                prefetched.add(url);
                const l = document.createElement('link');
                l.rel = 'prefetch';
                l.href = url;
                document.head.appendChild(l);
            }
        } catch (e) {}
    }
    document.addEventListener('mouseover', function(e) {
        const a = e.target.closest('a');
        if (a && a.href) prefetch(a.href);
    }, { passive: true });
    document.addEventListener('touchstart', function(e) {
        const a = e.target.closest('a');
        if (a && a.href) prefetch(a.href);
    }, { passive: true });
})();

// Universal Scroll Fade In Animation
const scrollObserverOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const scrollFadeObserver = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, scrollObserverOptions);

// Observe all scroll-fade-in elements
document.querySelectorAll('.scroll-fade-in').forEach(el => {
    scrollFadeObserver.observe(el);
});

// Scroll Animations (Fade-in on scroll) - Legacy support
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements with fade-in class
document.querySelectorAll('.card, .service-card, .project-card').forEach(el => {
    observer.observe(el);
});

// Header Behavior (Sticky, background change on scroll)
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;
    
    if (navbar) {
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
    
    lastScroll = currentScroll;
});

// Active Page Indicator
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath || 
            (currentPath === '/' && linkPath === '/') ||
            (currentPath.includes(linkPath) && linkPath !== '/')) {
            link.classList.add('active');
        }
    });
});

// Sticky Phone Bar (Mobile)
const stickyPhoneBar = document.querySelector('.sticky-phone-bar');
if (stickyPhoneBar) {
    window.addEventListener('scroll', function() {
        if (window.scrollY > 200) {
            stickyPhoneBar.style.display = 'block';
        } else {
            stickyPhoneBar.style.display = 'none';
        }
    });
}

// Click-to-Call Functionality (Mobile Detection)
function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

if (isMobile()) {
    document.querySelectorAll('a[href^="tel:"]').forEach(link => {
        link.addEventListener('click', function(e) {
            // Allow default behavior on mobile
        });
    });
}


// Form Validation Helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[0-9]{10}$/;
    return re.test(phone.replace(/\D/g, ''));
}

// Video Lazy Loading
document.querySelectorAll('video[data-src]').forEach(video => {
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                video.src = video.dataset.src;
                observer.unobserve(video);
            }
        });
    });
    observer.observe(video);
});

// Common Utility Functions
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

