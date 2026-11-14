// Testimonials page specific JavaScript

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
    
    // Testimonial Image Carousel Auto-Slide
    const testimonialCarousels = document.querySelectorAll('.project-image-carousel');
    testimonialCarousels.forEach(carousel => {
        const items = carousel.querySelectorAll('.carousel-image-item');
        if (items.length > 1) {
            let currentIndex = 0;
            
            setInterval(() => {
                items[currentIndex].classList.remove('active');
                currentIndex = (currentIndex + 1) % items.length;
                items[currentIndex].classList.add('active');
            }, 3000); // Change image every 3 seconds
        }
    });
});

