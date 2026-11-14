// Blog pages specific JavaScript

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
    
    // Blog Image Carousel Auto-Slide
    const blogCarousels = document.querySelectorAll('.project-image-carousel');
    blogCarousels.forEach(carousel => {
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
    
    // Related Posts Carousel (if using carousel)
    const relatedCarousel = document.querySelector('#relatedCarousel');
    if (relatedCarousel) {
        // Initialize Bootstrap carousel if needed
    }
    
    // Social Share Buttons
    const shareButtons = document.querySelectorAll('.share-btn');
    shareButtons.forEach(button => {
        button.addEventListener('click', function() {
            const platform = this.dataset.platform;
            const url = window.location.href;
            const title = document.title;
            
            let shareUrl = '';
            switch(platform) {
                case 'whatsapp':
                    shareUrl = `https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}`;
                    break;
                case 'facebook':
                    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
                    break;
                case 'twitter':
                    shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
                    break;
            }
            
            if (shareUrl) {
                window.open(shareUrl, '_blank', 'width=600,height=400');
            }
        });
    });

    // Copy URL Functionality
    const copyUrlButtons = document.querySelectorAll('.copy-url-btn');
    copyUrlButtons.forEach(button => {
        button.addEventListener('click', function() {
            const url = window.location.href;
            navigator.clipboard.writeText(url).then(() => {
                // Show success feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check"></i> Copied!';
                this.classList.add('btn-success');
                this.classList.remove('btn-outline-success');
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('btn-success');
                    this.classList.add('btn-outline-success');
                }, 2000);
            }).catch(err => {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = url;
                textArea.style.position = 'fixed';
                textArea.style.opacity = '0';
                document.body.appendChild(textArea);
                textArea.select();
                try {
                    document.execCommand('copy');
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="bi bi-check"></i> Copied!';
                    this.classList.add('btn-success');
                    this.classList.remove('btn-outline-success');
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('btn-success');
                        this.classList.add('btn-outline-success');
                    }, 2000);
                } catch (err) {
                    alert('Failed to copy URL. Please copy manually: ' + url);
                }
                document.body.removeChild(textArea);
            });
        });
    });
    
    // Reading Progress Indicator (optional)
    const blogContent = document.querySelector('.blog-content');
    if (blogContent) {
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress';
        progressBar.style.cssText = 'position: fixed; top: 0; left: 0; height: 3px; background: var(--primary-color); z-index: 9999; transition: width 0.1s;';
        document.body.appendChild(progressBar);
        
        window.addEventListener('scroll', function() {
            const windowHeight = window.innerHeight;
            const documentHeight = document.documentElement.scrollHeight;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const scrollPercent = (scrollTop / (documentHeight - windowHeight)) * 100;
            progressBar.style.width = scrollPercent + '%';
        });
    }
});

