// Services page specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Scroll Fade In Animation
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const scrollObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    const fadeElements = document.querySelectorAll('.scroll-fade-in');
    fadeElements.forEach(el => {
        scrollObserver.observe(el);
    });
});

