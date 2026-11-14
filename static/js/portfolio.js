// Portfolio page specific JavaScript

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
    
    const filterButtons = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('searchInput');
    
    // Filter Functionality
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            
            const category = this.dataset.category;
            filterProjects(category, searchInput.value);
        });
    });
    
    // Search Functionality
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            const activeFilter = document.querySelector('.filter-btn.active');
            const category = activeFilter ? activeFilter.dataset.category : 'all';
            filterProjects(category, this.value);
        }, 300));
    }
    
    // Filter Projects Function
    function filterProjects(category, searchTerm) {
        portfolioItems.forEach(item => {
            const itemCategory = item.dataset.category || '';
            const itemTitle = item.dataset.title || '';
            const itemLocation = item.dataset.location || '';
            
            const matchesCategory = category === 'all' || itemCategory.includes(category);
            const matchesSearch = !searchTerm || 
                itemTitle.includes(searchTerm.toLowerCase()) || 
                itemLocation.includes(searchTerm.toLowerCase());
            
            if (matchesCategory && matchesSearch) {
                item.classList.remove('hidden');
                setTimeout(() => {
                    item.style.opacity = '1';
                }, 10);
            } else {
                item.style.opacity = '0';
                setTimeout(() => {
                    item.classList.add('hidden');
                }, 300);
            }
        });
    }
    
    // Lightbox for Images (Simple modal)
    const galleryThumbnails = document.querySelectorAll('.gallery-thumbnail');
    galleryThumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            const imageSrc = this.dataset.image || this.src;
            const modalEl = document.getElementById('imageModal');
            if (window.bootstrap && modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                const modalImg = document.getElementById('modalImage');
                if (modalImg) modalImg.src = imageSrc;
                modal.show();
            }
        });
    });
    
    // Lazy Loading for Portfolio Images
    const portfolioImages = document.querySelectorAll('.portfolio-item img[loading="lazy"]');
    const imageObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                imageObserver.unobserve(img);
            }
        });
    });
    
    portfolioImages.forEach(img => {
        if (img.dataset.src) {
            imageObserver.observe(img);
        }
    });
    
    // URL Parameter Handling
    const urlParams = new URLSearchParams(window.location.search);
    const categoryParam = urlParams.get('category');
    if (categoryParam) {
        const button = document.querySelector(`[data-category="${categoryParam}"]`);
        if (button) {
            button.click();
        }
    }
    
    // Portfolio Grid Interactions
    portfolioItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
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

// Debounce function
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

