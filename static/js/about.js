/* ============================================
   ABOUT PAGE - JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    // Scroll fade-in animation
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: Stop observing after animation
                // observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all scroll-fade-in elements
    const fadeElements = document.querySelectorAll('.scroll-fade-in');
    fadeElements.forEach(el => {
        observer.observe(el);
    });
});

