// Project detail page specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Track project view via WebSocket
    const projectId = window.location.pathname.split('/').pop();
    if (projectId && !isNaN(projectId) && window.WebSocketClient) {
        window.WebSocketClient.trackProjectView(projectId);
    }
    
    // Before/After Slider Implementation
    const sliderContainer = document.querySelector('.slider-container');
    const sliderHandle = document.querySelector('.slider-handle');
    const afterImage = document.querySelector('.after-image');
    
    if (sliderContainer && sliderHandle && afterImage) {
        let isDragging = false;
        
        function updateSlider(percentage) {
            if (percentage >= 0 && percentage <= 100) {
                sliderHandle.style.left = percentage + '%';
                afterImage.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
            }
        }
        
        // Mouse events
        sliderHandle.addEventListener('mousedown', function(e) {
            isDragging = true;
            e.preventDefault();
        });
        
        document.addEventListener('mousemove', function(e) {
            if (!isDragging) return;
            
            const rect = sliderContainer.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const percentage = (x / rect.width) * 100;
            updateSlider(percentage);
        });
        
        document.addEventListener('mouseup', function() {
            isDragging = false;
        });
        
        // Touch events for mobile
        sliderHandle.addEventListener('touchstart', function(e) {
            isDragging = true;
            e.preventDefault();
        });
        
        document.addEventListener('touchmove', function(e) {
            if (!isDragging) return;
            
            const rect = sliderContainer.getBoundingClientRect();
            const x = e.touches[0].clientX - rect.left;
            const percentage = (x / rect.width) * 100;
            updateSlider(percentage);
        });
        
        document.addEventListener('touchend', function() {
            isDragging = false;
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (document.activeElement === sliderHandle || sliderContainer.contains(document.activeElement)) {
                let currentPos = parseFloat(sliderHandle.style.left) || 50;
                
                if (e.key === 'ArrowLeft') {
                    currentPos = Math.max(0, currentPos - 5);
                    updateSlider(currentPos);
                } else if (e.key === 'ArrowRight') {
                    currentPos = Math.min(100, currentPos + 5);
                    updateSlider(currentPos);
                }
            }
        });
        
        // Initialize slider at 50%
        updateSlider(50);
    }
    
    // Case Study Story Navigation
    const caseStudySteps = document.querySelectorAll('.case-study-step');
    if (caseStudySteps.length > 0) {
        // Add scroll spy for case study sections
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                }
            });
        }, { threshold: 0.3 });
        
        caseStudySteps.forEach(step => {
            observer.observe(step);
        });
    }
    
    // Image Gallery Lightbox with Next/Prev and Keyboard Support
    const galleryCards = document.querySelectorAll('.gallery-card');
    const imageModalEl = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const lightboxCounter = document.getElementById('lightboxCounter');
    const lightboxPrev = document.getElementById('lightboxPrev');
    const lightboxNext = document.getElementById('lightboxNext');
    
    const allGalleryImages = [];
    document.querySelectorAll('.gallery-card').forEach(card => {
        const src = card.getAttribute('data-image-src') || (card.querySelector('img') ? card.querySelector('img').src : '');
        if (src) {
            allGalleryImages.push(src);
        }
    });

    let currentLightboxIndex = 0;
    let bsModalInstance = null;

    function getModalInstance() {
        if (!bsModalInstance && imageModalEl && window.bootstrap) {
            bsModalInstance = bootstrap.Modal.getOrCreateInstance(imageModalEl);
        }
        return bsModalInstance;
    }

    function showLightboxImage(index) {
        if (!allGalleryImages.length) return;
        if (index < 0) index = allGalleryImages.length - 1;
        if (index >= allGalleryImages.length) index = 0;
        currentLightboxIndex = index;

        if (modalImage) {
            modalImage.src = allGalleryImages[currentLightboxIndex];
        }
        if (lightboxCounter) {
            lightboxCounter.textContent = `Photo ${currentLightboxIndex + 1} of ${allGalleryImages.length}`;
        }
    }

    galleryCards.forEach((card, idx) => {
        card.addEventListener('click', function() {
            showLightboxImage(idx);
            const m = getModalInstance();
            if (m) m.show();
        });

        card.addEventListener('mouseenter', function() {
            const overlay = this.querySelector('.gallery-hover-overlay');
            const img = this.querySelector('img');
            if (overlay) overlay.style.opacity = '1';
            if (img) img.style.transform = 'scale(1.08)';
        });

        card.addEventListener('mouseleave', function() {
            const overlay = this.querySelector('.gallery-hover-overlay');
            const img = this.querySelector('img');
            if (overlay) overlay.style.opacity = '0';
            if (img) img.style.transform = 'scale(1)';
        });
    });

    if (lightboxPrev) {
        lightboxPrev.addEventListener('click', function(e) {
            e.stopPropagation();
            showLightboxImage(currentLightboxIndex - 1);
        });
    }

    if (lightboxNext) {
        lightboxNext.addEventListener('click', function(e) {
            e.stopPropagation();
            showLightboxImage(currentLightboxIndex + 1);
        });
    }

    document.addEventListener('keydown', function(e) {
        if (!imageModalEl || !imageModalEl.classList.contains('show')) return;
        if (e.key === 'ArrowLeft') {
            showLightboxImage(currentLightboxIndex - 1);
        } else if (e.key === 'ArrowRight') {
            showLightboxImage(currentLightboxIndex + 1);
        }
    });
    
    // Related Projects Carousel (if using carousel)
    const relatedCarousel = document.querySelector('#relatedCarousel');
    if (relatedCarousel) {
        // Initialize if needed
    }
    
    // Social Share Functionality
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
});

