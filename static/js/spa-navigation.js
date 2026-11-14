/**
 * Balaji Marble Arts - Instant SPA Navigation Engine
 * Provides instant 0ms page transitions with client-side caching & smooth DOM swapping.
 */

(function() {
    'use strict';

    // In-memory HTML & parsed page cache
    const pageCache = new Map();
    let isNavigating = false;

    // Create and inject luxury top loading bar
    const progressBar = document.createElement('div');
    progressBar.id = 'spa-progress-bar';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        width: 0%;
        background: linear-gradient(90deg, #C6A15B, #F4D89E, #DFBA73);
        box-shadow: 0 0 10px rgba(198, 161, 91, 0.7);
        z-index: 999999;
        transition: width 0.2s ease, opacity 0.25s ease;
        opacity: 0;
        pointer-events: none;
    `;
    document.addEventListener('DOMContentLoaded', () => {
        document.body.appendChild(progressBar);
    });

    function startProgress() {
        progressBar.style.opacity = '1';
        progressBar.style.width = '25%';
        setTimeout(() => {
            if (isNavigating) progressBar.style.width = '70%';
        }, 80);
    }

    function finishProgress() {
        progressBar.style.width = '100%';
        setTimeout(() => {
            progressBar.style.opacity = '0';
            setTimeout(() => {
                progressBar.style.width = '0%';
            }, 250);
        }, 150);
    }

    // Cache current page on startup
    function cacheCurrentPage() {
        const currentUrl = window.location.pathname + window.location.search;
        const main = document.querySelector('main.main-content');
        if (main) {
            pageCache.set(currentUrl, {
                title: document.title,
                html: main.innerHTML,
                pageCss: Array.from(document.querySelectorAll('link[rel="stylesheet"]')).map(l => l.href)
            });
        }
    }

    // Fetch and cache a page
    async function fetchPage(url) {
        if (pageCache.has(url)) {
            return pageCache.get(url);
        }

        try {
            const res = await fetch(url, {
                headers: { 'X-Requested-With': 'SPA-Fetch' }
            });

            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const text = await res.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');

            const newMain = doc.querySelector('main.main-content');
            if (!newMain) return null;

            // Extract page-specific stylesheets
            const stylesheets = Array.from(doc.querySelectorAll('link[rel="stylesheet"]')).map(l => l.href);
            
            // Extract page-specific inline/external scripts
            const scripts = Array.from(doc.querySelectorAll('main script, body > script:not([src*="base"]):not([src*="bootstrap"])')).map(s => {
                return { src: s.src, content: s.innerHTML };
            });

            const pageData = {
                title: doc.title || document.title,
                html: newMain.innerHTML,
                stylesheets: stylesheets,
                scripts: scripts
            };

            pageCache.set(url, pageData);
            return pageData;
        } catch (e) {
            console.warn('SPA Fetch error:', e);
            return null;
        }
    }

    // Re-initialize dynamic components on newly loaded page
    function initPageInteractions() {
        // 1. Re-observe scroll fade-in elements
        const fadeElements = document.querySelectorAll('.scroll-fade-in');
        if (fadeElements.length > 0) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

            fadeElements.forEach(el => observer.observe(el));
        }

        // 2. Portfolio Page Filters & Search
        const filterButtons = document.querySelectorAll('.filter-btn');
        const searchInput = document.getElementById('searchInput');
        const portfolioItems = document.querySelectorAll('.portfolio-item');

        if (filterButtons.length > 0 && portfolioItems.length > 0) {
            filterButtons.forEach(btn => {
                btn.addEventListener('click', function() {
                    filterButtons.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    const category = this.dataset.category || 'all';
                    const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
                    filterPortfolio(category, query);
                });
            });

            if (searchInput) {
                searchInput.addEventListener('input', function() {
                    const activeBtn = document.querySelector('.filter-btn.active');
                    const category = activeBtn ? activeBtn.dataset.category : 'all';
                    filterPortfolio(category, this.value.toLowerCase().trim());
                });
            }

            function filterPortfolio(category, query) {
                portfolioItems.forEach(item => {
                    const itemCat = (item.dataset.category || '').toLowerCase();
                    const itemTitle = (item.dataset.title || '').toLowerCase();
                    const itemLoc = (item.dataset.location || '').toLowerCase();

                    const matchesCat = category === 'all' || itemCat.includes(category.toLowerCase());
                    const matchesQuery = !query || itemTitle.includes(query) || itemLoc.includes(query);

                    item.style.display = (matchesCat && matchesQuery) ? '' : 'none';
                });
            }
        }

        // 3. FAQ Accordion & Category Filter
        const faqSearch = document.getElementById('faqSearch');
        const catFilter = document.getElementById('categoryFilter');
        const faqItems = document.querySelectorAll('.faq-item');

        if (faqItems.length > 0) {
            function filterFaqs() {
                const query = (faqSearch ? faqSearch.value : '').toLowerCase().trim();
                const cat = (catFilter ? catFilter.value : 'all').toLowerCase();

                faqItems.forEach(item => {
                    const itemCat = (item.dataset.category || '').toLowerCase();
                    const q = (item.dataset.question || '').toLowerCase();
                    const a = (item.dataset.answer || '').toLowerCase();

                    const matchesCat = cat === 'all' || itemCat.includes(cat);
                    const matchesQuery = !query || q.includes(query) || a.includes(query);

                    item.style.display = (matchesCat && matchesQuery) ? '' : 'none';
                });
            }

            if (faqSearch) faqSearch.addEventListener('input', filterFaqs);
            if (catFilter) catFilter.addEventListener('change', filterFaqs);
        }

        // 4. Close mobile sidebar overlay if open
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        if (sidebar && sidebar.classList.contains('active')) {
            sidebar.classList.remove('active');
            if (overlay) overlay.classList.remove('active');
        }
        const navbarCollapse = document.querySelector('.navbar-collapse');
        if (navbarCollapse && navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        }

        // 5. Fire custom event for any other custom scripts
        window.dispatchEvent(new CustomEvent('page:swapped', { detail: { url: window.location.pathname } }));
    }

    // Update active state in navbars
    function updateActiveNav(pathname) {
        document.querySelectorAll('.navbar-nav .nav-link, .sidebar-nav-link').forEach(link => {
            const href = link.getAttribute('href');
            if (!href) return;
            const linkPath = href.split('?')[0].split('#')[0];
            if (linkPath === pathname || (pathname === '/' && (linkPath === '/' || linkPath === ''))) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // Execute DOM swap to new page
    async function navigateTo(url, pushState = true) {
        if (isNavigating) return;
        
        // If current URL is identical, just scroll top
        if (window.location.pathname + window.location.search === url) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            return;
        }

        isNavigating = true;
        startProgress();

        const mainContent = document.querySelector('main.main-content');
        if (mainContent) {
            mainContent.style.transition = 'opacity 0.12s ease';
            mainContent.style.opacity = '0.35';
        }

        const pageData = await fetchPage(url);

        if (!pageData) {
            // Fallback to normal navigation if fetch fails
            window.location.href = url;
            return;
        }

        // Inject any new stylesheets
        if (pageData.stylesheets) {
            pageData.stylesheets.forEach(href => {
                if (!document.querySelector(`link[href="${href}"]`)) {
                    const link = document.createElement('link');
                    link.rel = 'stylesheet';
                    link.href = href;
                    document.head.appendChild(link);
                }
            });
        }

        // Swap Content
        if (mainContent) {
            mainContent.innerHTML = pageData.html;
            document.title = pageData.title;

            if (pushState) {
                window.history.pushState({ url }, pageData.title, url);
            }

            updateActiveNav(window.location.pathname);
            window.scrollTo({ top: 0, behavior: 'instant' });

            // Fade back in
            requestAnimationFrame(() => {
                mainContent.style.opacity = '1';
                setTimeout(() => {
                    mainContent.style.transition = '';
                }, 150);
            });
        }

        // Execute any page-specific scripts
        if (pageData.scripts) {
            pageData.scripts.forEach(s => {
                const scriptEl = document.createElement('script');
                if (s.src) {
                    scriptEl.src = s.src;
                } else if (s.content) {
                    scriptEl.textContent = s.content;
                }
                document.body.appendChild(scriptEl);
            });
        }

        initPageInteractions();
        finishProgress();
        isNavigating = false;
    }

    // Click handler for intercepting internal navigation
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (!link) return;

        // Skip non-HTTP links, external links, downloads, new tabs
        const href = link.getAttribute('href');
        if (!href) return;
        if (href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:') || href.startsWith('javascript:')) return;
        if (link.getAttribute('target') === '_blank' || link.hasAttribute('download')) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

        // Only handle internal links
        try {
            const url = new URL(href, window.location.origin);
            if (url.origin !== window.location.origin) return;
            if (url.pathname.startsWith('/admin') || url.pathname.startsWith('/static')) return;

            e.preventDefault();
            navigateTo(url.pathname + url.search);
        } catch (err) {}
    });

    // Touch / Pointer head-start (fetches page into cache 100ms before click completes)
    document.addEventListener('pointerdown', function(e) {
        const link = e.target.closest('a');
        if (!link) return;
        const href = link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:')) return;
        try {
            const url = new URL(href, window.location.origin);
            if (url.origin === window.location.origin && !url.pathname.startsWith('/admin') && !url.pathname.startsWith('/static')) {
                const target = url.pathname + url.search;
                if (!pageCache.has(target)) {
                    fetchPage(target); // Prefetch quietly into RAM
                }
            }
        } catch (err) {}
    }, { passive: true });

    // Handle Browser Back / Forward buttons
    window.addEventListener('popstate', function(e) {
        const url = window.location.pathname + window.location.search;
        navigateTo(url, false);
    });

    // Background pre-cache of all main navigation routes (runs when idle)
    function backgroundPreload() {
        const coreRoutes = [
            '/',
            '/portfolio',
            '/services',
            '/materials',
            '/about',
            '/faq',
            '/blog',
            '/contact'
        ];

        let index = 0;
        function loadNext() {
            if (index >= coreRoutes.length) return;
            const route = coreRoutes[index++];
            if (route !== window.location.pathname && !pageCache.has(route)) {
                fetchPage(route).then(() => {
                    setTimeout(loadNext, 120); // Quiet 120ms interval
                });
            } else {
                loadNext();
            }
        }

        // Start 800ms after initial page load
        setTimeout(loadNext, 800);
    }

    // Startup initialization
    window.addEventListener('DOMContentLoaded', () => {
        cacheCurrentPage();
        initPageInteractions();
        backgroundPreload();
    });

})();

