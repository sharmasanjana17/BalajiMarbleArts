// Materials page specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const materialTypeFilter = document.getElementById('materialTypeFilter');
    const finishFilter = document.getElementById('finishFilter');
    const materialItems = document.querySelectorAll('.material-item');
    
    // Material Filtering
    function filterMaterials() {
        const typeValue = materialTypeFilter ? materialTypeFilter.value : 'all';
        const finishValue = finishFilter ? finishFilter.value.toLowerCase() : 'all';
        
        materialItems.forEach(item => {
            const itemType = item.dataset.type || '';
            const itemFinishes = item.dataset.finishes || '';
            
            const matchesType = typeValue === 'all' || itemType === typeValue;
            const matchesFinish = finishValue === 'all' || itemFinishes.includes(finishValue);
            
            if (matchesType && matchesFinish) {
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
    
    if (materialTypeFilter) {
        materialTypeFilter.addEventListener('change', filterMaterials);
    }
    
    if (finishFilter) {
        finishFilter.addEventListener('change', filterMaterials);
    }
    
    // Material Comparison Tool
    const compareButtons = document.querySelectorAll('.compare-btn');
    const selectedMaterials = [];
    
    compareButtons.forEach(button => {
        button.addEventListener('click', function() {
            const materialId = this.dataset.materialId;
            const materialCard = this.closest('.material-card');
            
            if (selectedMaterials.includes(materialId)) {
                // Remove from comparison
                selectedMaterials.splice(selectedMaterials.indexOf(materialId), 1);
                materialCard.classList.remove('selected-for-comparison');
            } else {
                // Add to comparison
                if (selectedMaterials.length < 2) {
                    selectedMaterials.push(materialId);
                    materialCard.classList.add('selected-for-comparison');
                } else {
                    if (typeof showMessage === 'function') {
                        showMessage('You can compare maximum 2 materials at a time', 'warning');
                    } else {
                        alert('You can compare maximum 2 materials at a time');
                    }
                }
            }
            
            if (selectedMaterials.length === 2) {
                // Show comparison modal or section
                showComparison(selectedMaterials);
            }
        });
    });
    
    function showComparison(materialIds) {
        // Implement comparison display
        console.log('Comparing materials:', materialIds);
    }
    
    // Image Gallery for Materials
    const materialImages = document.querySelectorAll('.material-card img');
    materialImages.forEach(img => {
        img.addEventListener('click', function() {
            // Open lightbox or modal
            const modalEl = document.getElementById('imageModal');
            if (window.bootstrap && modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                const modalImg = document.getElementById('modalImage');
                if (modalImg) modalImg.src = this.src;
                modal.show();
            }
        });
    });
    
    // Lightbox for Material Samples
    const sampleButtons = document.querySelectorAll('.sample-btn');
    sampleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const imageSrc = this.dataset.image;
            const modalEl = document.getElementById('imageModal');
            if (imageSrc && window.bootstrap && modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                const modalImg = document.getElementById('modalImage');
                if (modalImg) modalImg.src = imageSrc;
                modal.show();
            }
        });
    });
    
    // Search Functionality
    const searchInput = document.getElementById('materialSearch');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            const searchTerm = this.value.toLowerCase();
            materialItems.forEach(item => {
                const materialName = item.querySelector('.card-title').textContent.toLowerCase();
                const materialDesc = item.querySelector('.card-text').textContent.toLowerCase();
                
                if (materialName.includes(searchTerm) || materialDesc.includes(searchTerm)) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
        }, 300));
    }
    
    // Material Card Interactions
    materialItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
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

