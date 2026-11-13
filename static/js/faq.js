// FAQ page specific JavaScript

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
    
    const categoryFilter = document.getElementById('categoryFilter');
    const faqSearch = document.getElementById('faqSearch');
    const faqItems = document.querySelectorAll('.faq-item');
    
    // Accordion Functionality (Bootstrap handles this, but we can add custom behavior)
    const accordionButtons = document.querySelectorAll('.accordion-button');
    accordionButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Add any custom behavior here
        });
    });
    
    // FAQ Search Functionality
    if (faqSearch) {
        faqSearch.addEventListener('input', debounce(function() {
            const searchTerm = this.value.toLowerCase();
            filterFAQs(categoryFilter ? categoryFilter.value : 'all', searchTerm);
        }, 300));
    }
    
    // Category Filtering
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            const searchTerm = faqSearch ? faqSearch.value.toLowerCase() : '';
            filterFAQs(this.value, searchTerm);
        });
    }
    
    // Filter FAQs Function
    function filterFAQs(category, searchTerm) {
        let visibleCount = 0;
        
        faqItems.forEach(item => {
            const itemCategory = item.dataset.category || '';
            const itemQuestion = item.dataset.question || '';
            const itemAnswer = item.dataset.answer || '';
            
            const matchesCategory = category === 'all' || itemCategory === category;
            const matchesSearch = !searchTerm || 
                itemQuestion.includes(searchTerm) || 
                itemAnswer.includes(searchTerm);
            
            if (matchesCategory && matchesSearch) {
                item.classList.remove('hidden');
                visibleCount++;
            } else {
                item.classList.add('hidden');
            }
        });
        
        // Show message if no results
        const noResultsMsg = document.getElementById('noResults');
        if (visibleCount === 0) {
            if (!noResultsMsg) {
                const msg = document.createElement('div');
                msg.id = 'noResults';
                msg.className = 'alert alert-info text-center';
                msg.textContent = 'No FAQs found matching your search.';
                document.querySelector('.accordion').parentNode.insertBefore(msg, document.querySelector('.accordion'));
            }
        } else {
            if (noResultsMsg) {
                noResultsMsg.remove();
            }
        }
    }
    
    // Smooth Animations
    faqItems.forEach(item => {
        item.style.transition = 'opacity 0.3s ease';
    });
    
    // FAQ Interactions
    const accordionItems = document.querySelectorAll('.accordion-item');
    accordionItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        item.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
});

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

