/**
 * Blue Envelope Program - Professional Website JavaScript
 * WCAG 2.1 AA Compliant & Fully Accessible
 */

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeMobileMenu();
    initializeSmoothScrolling();
    initializeScrollAnimations();
    initializeCounterAnimations();
    initializeChartInteractions();
    initializeRippleEffects();
    initializeAccessibilityFeatures();
});

/**
 * Mobile Menu Functionality
 */
function initializeMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (!mobileToggle || !navMenu) return;
    
    mobileToggle.addEventListener('click', function() {
        const isExpanded = mobileToggle.getAttribute('aria-expanded') === 'true';
        
        // Toggle menu visibility
        navMenu.classList.toggle('active');
        mobileToggle.setAttribute('aria-expanded', !isExpanded);
        
        // Update button text for screen readers
        const buttonText = !isExpanded ? 'Close mobile menu' : 'Open mobile menu';
        mobileToggle.setAttribute('aria-label', buttonText);
        
        // Prevent body scroll when menu is open
        document.body.style.overflow = !isExpanded ? 'hidden' : '';
        
        // Close menu when clicking outside
        if (!isExpanded) {
            document.addEventListener('click', closeMenuOnOutsideClick);
        } else {
            document.removeEventListener('click', closeMenuOnOutsideClick);
        }
    });
    
    // Close menu when clicking on nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            mobileToggle.setAttribute('aria-expanded', 'false');
            mobileToggle.setAttribute('aria-label', 'Open mobile menu');
            document.body.style.overflow = '';
        });
    });
    
    function closeMenuOnOutsideClick(event) {
        if (!navMenu.contains(event.target) && !mobileToggle.contains(event.target)) {
            navMenu.classList.remove('active');
            mobileToggle.setAttribute('aria-expanded', 'false');
            mobileToggle.setAttribute('aria-label', 'Open mobile menu');
            document.body.style.overflow = '';
            document.removeEventListener('click', closeMenuOnOutsideClick);
        }
    }
}

/**
 * Smooth Scrolling for Anchor Links
 */
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if it's just "#"
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (!target) return;
            
            e.preventDefault();
            
            // Calculate offset for fixed header
            const headerHeight = document.querySelector('.header').offsetHeight;
            const targetPosition = target.offsetTop - headerHeight - 20;
            
            // Smooth scroll to target
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
            
            // Update focus for accessibility
            target.setAttribute('tabindex', '-1');
            target.focus();
            target.removeAttribute('tabindex');
        });
    });
}

/**
 * Scroll-triggered Animations
 */
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Add staggered animation delays for multiple elements
                const siblings = Array.from(entry.target.parentNode.children);
                const index = siblings.indexOf(entry.target);
                entry.target.style.animationDelay = `${index * 0.1}s`;
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll(
        '.stat-card, .analysis-card, .chart-card, .visual-item, .card, h2, h3'
    );
    
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

/**
 * Counter Animations for Statistics
 */
function initializeCounterAnimations() {
    const counters = document.querySelectorAll('.stat-number');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseInt(element.textContent);
    const duration = 2000; // 2 seconds
    const increment = target / (duration / 16); // 60fps
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

/**
 * Chart and Card Interactions
 */
function initializeChartInteractions() {
    const chartCards = document.querySelectorAll('.chart-card');
    
    chartCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        // Add keyboard support
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        // Make cards focusable
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
    });
}

/**
 * Ripple Effect for Buttons
 */
function initializeRippleEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            createRippleEffect(e, this);
        });
    });
}

function createRippleEffect(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

/**
 * Accessibility Features
 */
function initializeAccessibilityFeatures() {
    // Add focus indicators for keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
    
    // Improve form accessibility
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        if (!input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')) {
            const label = input.previousElementSibling;
            if (label && label.tagName === 'LABEL') {
                input.setAttribute('aria-labelledby', label.id || 'label-' + Math.random().toString(36).substr(2, 9));
            }
        }
    });
    
    // Add skip link functionality
    const skipLink = document.querySelector('.skip-link');
    if (skipLink) {
        skipLink.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.setAttribute('tabindex', '-1');
                target.focus();
                target.removeAttribute('tabindex');
            }
        });
    }
}

/**
 * Chart Modal Functions
 */
function openChartModal(imageSrc, caption) {
    const modal = document.getElementById('chartModal');
    const modalImage = document.getElementById('modalChartImage');
    const modalCaption = document.getElementById('modalChartCaption');
    
    if (modal && modalImage && modalCaption) {
        modalImage.src = imageSrc;
        modalImage.alt = caption;
        modalCaption.textContent = caption;
        modal.style.display = 'block';
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
        
        // Focus management for accessibility
        modal.setAttribute('aria-hidden', 'false');
        const closeButton = modal.querySelector('.chart-modal-close');
        if (closeButton) {
            closeButton.focus();
        }
    }
}

function closeChartModal() {
    const modal = document.getElementById('chartModal');
    
    if (modal) {
        modal.style.display = 'none';
        
        // Restore body scroll
        document.body.style.overflow = '';
        
        // Focus management for accessibility
        modal.setAttribute('aria-hidden', 'true');
        
        // Return focus to the chart that was clicked
        const activeElement = document.activeElement;
        if (activeElement && activeElement.classList.contains('clickable-chart')) {
            activeElement.focus();
        }
    }
}

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeChartModal();
    }
});

/**
 * Utility Functions
 */

// Debounce function for performance optimization
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

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Check if user prefers reduced motion
function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .keyboard-navigation *:focus {
        outline: 2px solid var(--accent-blue) !important;
        outline-offset: 2px !important;
    }
    
    @media (prefers-reduced-motion: reduce) {
        .ripple {
            display: none;
        }
        
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
`;
document.head.appendChild(style);