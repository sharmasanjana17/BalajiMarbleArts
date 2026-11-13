// Mobile Navigation Drawer Functionality

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const navbarSidebarToggle = document.getElementById('navbarSidebarToggle');
    const sidebarToggle = document.getElementById('sidebarToggle');
    
    // Clear any legacy desktop state
    localStorage.removeItem('sidebarOpen');

    function checkViewport() {
        if (window.innerWidth >= 992) {
            closeSidebar();
        }
    }

    // Always start closed
    closeSidebar();
    checkViewport();

    function openSidebar() {
        // Never open on desktop
        if (window.innerWidth >= 992) {
            closeSidebar();
            return;
        }

        document.body.classList.add('sidebar-open');
        if (sidebar) {
            sidebar.classList.remove('hidden');
            sidebar.classList.add('active');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.add('active');
        }
    }

    function closeSidebar() {
        document.body.classList.remove('sidebar-open');
        if (sidebar) {
            sidebar.classList.add('hidden');
            sidebar.classList.remove('active');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.remove('active');
        }

        // Clean any leftover desktop shift classes
        const shiftElements = ['.navbar', '.sticky-phone-bar', 'main', 'footer'];
        shiftElements.forEach(sel => {
            const el = document.querySelector(sel);
            if (el) el.classList.remove('sidebar-open');
        });
    }

    function toggleSidebar() {
        if (sidebar && sidebar.classList.contains('active')) {
            closeSidebar();
        } else {
            openSidebar();
        }
    }

    // Bind mobile navbar toggler
    if (navbarSidebarToggle) {
        navbarSidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleSidebar();
        });
    }

    // Bind legacy toggle if present
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleSidebar();
        });
    }

    // Close button
    if (sidebarClose) {
        sidebarClose.addEventListener('click', function() {
            closeSidebar();
        });
    }

    // Close on overlay click
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            closeSidebar();
        });
    }

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeSidebar();
        }
    });

    // Check viewport on resize
    window.addEventListener('resize', checkViewport);

    // Auto-close when clicking any link inside sidebar
    document.querySelectorAll('.sidebar-menu-link, .sidebar-action-btn').forEach(link => {
        link.addEventListener('click', function() {
            closeSidebar();
        });
    });

    // Set active menu item based on current page
    setActiveMenuItem();

    function setActiveMenuItem() {
        const currentPath = window.location.pathname;
        const menuLinks = document.querySelectorAll('.sidebar-menu-link');
        
        menuLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPath || (currentPath === '/' && href === '/')) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
});
