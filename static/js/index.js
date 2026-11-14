// Home page specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Subscribe to notifications
    if (window.WebSocketClient) {
        window.WebSocketClient.subscribeToNotifications('guest');
    }
    
    // Hero Section Animations
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        setTimeout(() => {
            heroContent.classList.add('fade-in');
        }, 100);
    }
    
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
    
    // Hero Scroll Indicator Click
    const scrollIndicator = document.querySelector('.hero-scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', function() {
            window.scrollTo({
                top: window.innerHeight,
                behavior: 'smooth'
            });
        });
    }
    
    // Testimonials Carousel
    const testimonialsCarousel = document.querySelector('#testimonialsCarousel');
    if (testimonialsCarousel) {
        // Bootstrap carousel will handle auto-rotation
    }
    
    // Trust Badge Counter Animation
    const trustCounters = document.querySelectorAll('.trust-counter');
    const counterObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'));
                const suffix = counter.textContent.includes('+') ? '+' : '';
                
                if (target && !isNaN(target)) {
                    counter.classList.add('animated');
                    let current = 0;
                    const duration = 2000; // 2 seconds
                    const increment = target / (duration / 16); // 60fps
                    
                    const updateCounter = () => {
                        current += increment;
                        if (current < target) {
                            counter.textContent = Math.floor(current) + suffix;
                            requestAnimationFrame(updateCounter);
                        } else {
                            counter.textContent = target + suffix;
                        }
                    };
                    
                    updateCounter();
                }
            }
        });
    }, { threshold: 0.5 });
    
    trustCounters.forEach(counter => {
        counterObserver.observe(counter);
    });
    
    // Video Autoplay on Hover
    const projectVideos = document.querySelectorAll('.project-media');
    projectVideos.forEach(media => {
        if (media.tagName === 'VIDEO') {
            const video = media;
            
            // Play on hover
            media.closest('.project-card')?.addEventListener('mouseenter', function() {
                video.play().catch(e => {
                    // Autoplay might be blocked, that's okay
                    console.log('Video autoplay prevented:', e);
                });
            });
            
            // Pause on leave
            media.closest('.project-card')?.addEventListener('mouseleave', function() {
                video.pause();
                video.currentTime = 0;
            });
        }
    });
    
    // Process Section Stagger Animation
    const processSteps = document.querySelectorAll('.process-step');
    const processObserver = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                entry.target.classList.add('animated');
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 150);
            }
        });
    }, { threshold: 0.2 });
    
    // Project Image Carousel Auto-Slide
    const projectCarousels = document.querySelectorAll('.project-image-carousel');
    projectCarousels.forEach(carousel => {
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
