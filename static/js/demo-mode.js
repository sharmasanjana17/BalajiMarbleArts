// Demo mode for on-site presentations

document.addEventListener('DOMContentLoaded', function() {
    // Check if demo mode is enabled via URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const isDemoMode = urlParams.get('demo') === 'true';
    
    if (isDemoMode) {
        enableDemoMode();
    }
    
    function enableDemoMode() {
        // Add demo mode class to body
        document.body.classList.add('demo-mode');
        
        // Hide navigation and footer
        const navbar = document.querySelector('.navbar');
        const footer = document.querySelector('footer');
        
        if (navbar) navbar.style.display = 'none';
        if (footer) footer.style.display = 'none';
        
        // Add full-screen toggle button
        const fullscreenBtn = document.createElement('button');
        fullscreenBtn.className = 'btn btn-primary demo-fullscreen-btn';
        fullscreenBtn.innerHTML = '<i class="bi bi-fullscreen"></i>';
        fullscreenBtn.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 10000; border-radius: 50%; width: 50px; height: 50px;';
        document.body.appendChild(fullscreenBtn);
        
        fullscreenBtn.addEventListener('click', toggleFullscreen);
        
        // Touch gesture handling
        let touchStartX = 0;
        let touchStartY = 0;
        
        document.addEventListener('touchstart', function(e) {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        });
        
        document.addEventListener('touchend', function(e) {
            if (!touchStartX || !touchStartY) return;
            
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            const diffX = touchStartX - touchEndX;
            const diffY = touchStartY - touchEndY;
            
            // Swipe left/right for navigation
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    // Swipe left - next project
                    navigateProject('next');
                } else {
                    // Swipe right - previous project
                    navigateProject('prev');
                }
            }
            
            touchStartX = 0;
            touchStartY = 0;
        });
    }
    
    function toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.log('Error attempting to enable fullscreen:', err);
            });
        } else {
            document.exitFullscreen();
        }
    }
    
    function navigateProject(direction) {
        // Implement project navigation logic
        console.log('Navigate', direction);
    }
    
    // QR Code Generation (simple implementation)
    function generateQRCode(text) {
        // Use a QR code library or API
        // For now, just return a placeholder
        return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(text)}`;
    }
});

