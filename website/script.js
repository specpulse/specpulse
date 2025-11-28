// Smooth scroll functionality
function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Copy code functionality
function copyCode(button) {
    const codeBlock = button.closest('.code-block');
    const code = codeBlock.querySelector('code');
    const text = code.textContent;

    navigator.clipboard.writeText(text).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copied!';
        button.classList.add('text-green-500');

        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.classList.remove('text-green-500');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy code:', err);
    });
}

// Install SpecPulse function
function installSpecPulse() {
    const command = 'pip install specpulse';
    navigator.clipboard.writeText(command).then(() => {
        showNotification('Command copied to clipboard! Paste it in your terminal.', 'success');
    }).catch(err => {
        console.error('Failed to copy command:', err);
        showNotification('Failed to copy command. Please copy manually: pip install specpulse', 'error');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 flex items-center space-x-2 ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        'bg-blue-500 text-white'
    }`;

    const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ';
    notification.innerHTML = `
        <span class="text-lg">${icon}</span>
        <span>${message}</span>
    `;

    document.body.appendChild(notification);

    // Animate in
    notification.style.transform = 'translateY(100%)';
    notification.style.opacity = '0';
    notification.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';

    setTimeout(() => {
        notification.style.transform = 'translateY(0)';
        notification.style.opacity = '1';
    }, 10);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateY(100%)';
        notification.style.opacity = '0';

        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe scroll-animate elements
document.addEventListener('DOMContentLoaded', () => {
    const scrollElements = document.querySelectorAll('.scroll-animate');
    scrollElements.forEach(el => observer.observe(el));

    // Add scroll-animate class to elements that should animate
    const animateElements = document.querySelectorAll('.feature-card, .showcase-card, .doc-card, .platform-card');
    animateElements.forEach(el => {
        el.classList.add('scroll-animate');
        observer.observe(el);
    });
});

// Typing animation for terminal
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

// Enhanced mobile menu
document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    }
});

// Add floating particles to hero section
function createParticle() {
    const particle = document.createElement('div');
    particle.className = 'particle';

    const size = Math.random() * 4 + 2;
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    particle.style.background = 'rgba(139, 92, 246, 0.6)';
    particle.style.borderRadius = '50%';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
    particle.style.animationDelay = Math.random() * 2 + 's';

    const hero = document.querySelector('.hero');
    if (hero) {
        hero.appendChild(particle);

        // Remove particle after animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 8000);
    }
}

// Create particles periodically
setInterval(createParticle, 1000);

// Smooth parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroVisual = document.querySelector('.hero-visual');

    if (heroVisual) {
        const speed = 0.5;
        heroVisual.style.transform = `translateY(${scrolled * speed}px)`;
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus command palette (if implemented)
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        // Focus search or command input
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="search"], input[placeholder*="Search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }

    // Escape to close modals/menus
    if (e.key === 'Escape') {
        const activeMenu = document.querySelector('.nav-menu.active, .modal.active');
        if (activeMenu) {
            activeMenu.classList.remove('active');
        }
    }
});

// Performance optimization - Debounce scroll events
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

// Apply debouncing to scroll handlers
const debouncedScrollHandler = debounce(() => {
    // Scroll-based animations or calculations
}, 16); // ~60fps

window.addEventListener('scroll', debouncedScrollHandler);

// Add loading states to buttons
document.addEventListener('click', (e) => {
    if (e.target.matches('button[type="submit"], .btn-primary')) {
        const button = e.target;

        // Don't add loading state if already loading
        if (button.classList.contains('loading')) {
            return;
        }

        button.classList.add('loading');

        // Remove loading state after 2 seconds (customize as needed)
        setTimeout(() => {
            button.classList.remove('loading');
        }, 2000);
    }
});

// Initialize tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = e.target.dataset.tooltip;
            tooltip.style.cssText = `
                position: absolute;
                background: rgba(0, 0, 0, 0.9);
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 14px;
                z-index: 1000;
                pointer-events: none;
                white-space: nowrap;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                margin-bottom: 8px;
            `;

            e.target.style.position = 'relative';
            e.target.appendChild(tooltip);

            // Fade in animation
            requestAnimationFrame(() => {
                tooltip.style.opacity = '1';
                tooltip.style.transform = 'translateX(-50%) translateY(-4px)';
            });
        });

        element.addEventListener('mouseleave', (e) => {
            const tooltip = e.target.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initTooltips();

    // Add fade-in animation to body
    document.body.style.opacity = '0';
    requestAnimationFrame(() => {
        document.body.style.transition = 'opacity 0.5s ease-in-out';
        document.body.style.opacity = '1';
    });
});

// Add pulse animation to CTA elements
function addPulseAnimation() {
    const ctaElements = document.querySelectorAll('.cta-action, .btn-primary');

    ctaElements.forEach(element => {
        if (Math.random() > 0.7) { // 30% chance to add pulse
            element.style.animation = 'pulse-glow 2s ease-in-out infinite';
        }
    });
}

// Call pulse animation periodically
setInterval(addPulseAnimation, 5000);

// Export functions for external use
window.SpecPulseWebsite = {
    scrollToSection,
    copyCode,
    installSpecPulse,
    showNotification
};