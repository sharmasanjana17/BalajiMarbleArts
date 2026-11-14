/**
 * Balaji Marble Arts - Ultra-Fast Instant SPA Engine
 * Uses in-memory Map & SessionStorage caching for 0ms page changes.
 */

(function() {
    'use strict';

    const memoryCache = new Map();
    let isNavigating = false;

    // Golden luxury progress bar
    const progressBar = document.createElement('div');
    progressBar.id = 'spa-progress-bar';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        width: 0%;
        background: linear-gradient(90deg, #C6A15B, #F4D89E, #C6A15B);
        box-shadow: 0 0 10px rgba(198, 161, 91, 0.8);
        z-index: 999999;
        transition: width 0.15s ease, opacity 0.2s ease;
        opacity: 0;
        pointer-events: none;
    `;

    function startProgress() {
        progressBar.style.opacity = '1';
        progressBar.style.width = '35%';
        setTimeout(() => {
            if (isNavigating) progressBar.style.width = '75%';
        }, 50);
    }

    function finishProgress() {
        progressBar.style.width = '100%';
        setTimeout(() => {
            progressBar.style.opacity = '0';
            setTimeout(() => {
                progressBar.style.width = '0%';
            }, 200);
        }, 120);
    }

    // Storage cache helpers
    function getCached(url) {
        if (memoryCache.has(url)) return memoryCache.get(url);
        try {
            const stored = sessionStorage.getItem('bma_spa_' + url);
            if (stored) {
                const parsed = JSON.parse(stored);
                memoryCache.set(url, parsed);
                return parsed;
            }
        } catch (e) {}
        return null;
    }

    function setCached(url, data) {
        memoryCache.set(url, data);
        try {
            sessionStorage.setItem('bma_spa_' + url, JSON.stringify(data));
        } catch (e) {}
    }

    function cacheCurrentPage() {
        const url = window.location.pathname + window.location.search;
        const main = document.querySelector('main.main-content');
        if (main && !getCached(url)) {
            setCached(url, {
                title: document.title,
                html: main.innerHTML,
                stylesheets: Array.from(document.querySelectorAll('link[rel="stylesheet"]')).map(l => l.href)
            });
        }
    }

    // Fetch page HTML without custom headers to avoid CORS preflight
    async function fetchPage(url) {
        const cached = getCached(url);
        if (cached) return cached;

        try {
            const res = await fetch(url, {
                method: 'GET',
                credentials: 'same-origin',
                headers: { 'Accept': 'text/html' }
            });

            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            const text = await res.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');

            const newMain = doc.querySelector('main.main-content');
            if (!newMain) return null;

            const stylesheets = Array.from(doc.querySelectorAll('link[rel="stylesheet"]')).map(l => l.href);
            const scripts = Array.from(doc.querySelectorAll('main script, body > script:not([src*="base"]):not([src*="bootstrap"])')).map(s => {
                return { src: s.src, content: s.innerHTML };
            });

            const pageData = {
                title: doc.title || document.title,
                html: newMain.innerHTML,
                stylesheets: stylesheets,
                scripts: scripts
            };

            setCached(url, pageData);
            return pageData;
        } catch (err) {
            console.warn('SPA fetch fallback:', err);
            return null;
        }
    }

    // Re-initialize dynamic interactions on new page
    function initPageInteractions() {
        // Observe scroll fade-in
        const fadeElements = document.querySelectorAll('.scroll-fade-in');
        if (fadeElements.length > 0) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) entry.target.classList.add('visible');
                });
            }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
            fadeElements.forEach(el => observer.observe(el));
        }

        // Portfolio filtering
        const filterButtons = document.querySelectorAll('.filter-btn');
        const searchInput = document.getElementById('searchInput');
        const portfolioItems = document.querySelectorAll('.portfolio-item');

        if (filterButtons.length > 0 && portfolioItems.length > 0) {
            filterButtons.forEach(btn => {
                btn.addEventListener('click', function() {
                    filterButtons.forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    filterProjects();
                });
            });

            if (searchInput) {
                searchInput.addEventListener('input', filterProjects);
            }

            function filterProjects() {
                const activeBtn = document.querySelector('.filter-btn.active');
                const cat = (activeBtn ? activeBtn.dataset.category : 'all').toLowerCase();
                const q = (searchInput ? searchInput.value : '').toLowerCase().trim();

                portfolioItems.forEach(item => {
                    const itemCat = (item.dataset.category || '').toLowerCase();
                    const itemTitle = (item.dataset.title || '').toLowerCase();
                    const itemLoc = (item.dataset.location || '').toLowerCase();

                    const matchesCat = cat === 'all' || itemCat.includes(cat);
                    const matchesQ = !q || itemTitle.includes(q) || itemLoc.includes(q);

                    item.style.display = (matchesCat && matchesQ) ? '' : 'none';
                });
            }
        }

        // Close mobile sidebar and collapses
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

        window.dispatchEvent(new CustomEvent('page:swapped', { detail: { url: window.location.pathname } }));
    }

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

    // Instant Page Swap
    async function navigateTo(url, pushState = true) {
        if (isNavigating) return;

        if (window.location.pathname + window.location.search === url) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            return;
        }

        isNavigating = true;
        startProgress();

        const mainContent = document.querySelector('main.main-content');
        if (mainContent) {
            mainContent.style.transition = 'opacity 0.08s ease';
            mainContent.style.opacity = '0.4';
        }

        const pageData = await fetchPage(url);

        if (!pageData) {
            window.location.href = url;
            return;
        }

        // Append new stylesheets if any
        if (pageData.stylesheets) {
            pageData.stylesheets.forEach(href => {
                if (!document.querySelector(`link[href="${href}"]`)) {
                    const l = document.createElement('link');
                    l.rel = 'stylesheet';
                    l.href = href;
                    document.head.appendChild(l);
                }
            });
        }

        // Swap Content Instantly
        if (mainContent) {
            mainContent.innerHTML = pageData.html;
            document.title = pageData.title;

            if (pushState) {
                window.history.pushState({ url }, pageData.title, url);
            }

            updateActiveNav(window.location.pathname);
            window.scrollTo({ top: 0, behavior: 'instant' });

            requestAnimationFrame(() => {
                mainContent.style.opacity = '1';
                setTimeout(() => {
                    mainContent.style.transition = '';
                }, 100);
            });
        }

        // Execute scripts
        if (pageData.scripts) {
            pageData.scripts.forEach(s => {
                const scriptEl = document.createElement('script');
                if (s.src) scriptEl.src = s.src;
                else if (s.content) scriptEl.textContent = s.content;
                document.body.appendChild(scriptEl);
            });
        }

        initPageInteractions();
        finishProgress();
        isNavigating = false;
    }

    // Intercept clicks on links
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (!link) return;

        const href = link.getAttribute('href');
        if (!href) return;
        if (href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:') || href.startsWith('javascript:')) return;
        if (link.getAttribute('target') === '_blank' || link.hasAttribute('download')) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

        try {
            const targetUrl = new URL(href, window.location.origin);
            if (targetUrl.origin !== window.location.origin) return;
            if (targetUrl.pathname.startsWith('/admin') || targetUrl.pathname.startsWith('/static')) return;

            e.preventDefault();
            navigateTo(targetUrl.pathname + targetUrl.search);
        } catch (err) {}
    });

    // Tap/Pointer prefetch (100ms head start before click completes)
    document.addEventListener('pointerdown', function(e) {
        const link = e.target.closest('a');
        if (!link) return;
        const href = link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:')) return;
        try {
            const targetUrl = new URL(href, window.location.origin);
            if (targetUrl.origin === window.location.origin && !targetUrl.pathname.startsWith('/admin')) {
                const path = targetUrl.pathname + targetUrl.search;
                if (!getCached(path)) {
                    fetchPage(path);
                }
            }
        } catch (err) {}
    }, { passive: true });

    // Browser back / forward buttons
    window.addEventListener('popstate', function() {
        const url = window.location.pathname + window.location.search;
        navigateTo(url, false);
    });

    // Quiet background preload of all main routes
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
            const r = coreRoutes[index++];
            if (r !== window.location.pathname && !getCached(r)) {
                fetchPage(r).then(() => {
                    setTimeout(loadNext, 100);
                });
            } else {
                loadNext();
            }
        }
        setTimeout(loadNext, 500);
    }

    // Immediate and infallible initialization
    function init() {
        if (!document.body.contains(progressBar)) {
            document.body.appendChild(progressBar);
        }
        cacheCurrentPage();
        initPageInteractions();
        backgroundPreload();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
