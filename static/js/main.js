/* ==============================================================
   NayePankh Foundation - Main JavaScript
   Handles animations, form validation, and dynamic interactions
   ============================================================== */

document.addEventListener('DOMContentLoaded', function() {

    // ==============================================================
    // NAVBAR SCROLL EFFECT
    // ==============================================================
    // Changes navbar appearance when user scrolls down
    const navbar = document.getElementById('mainNavbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // ==============================================================
    // AUTO-DISMISS ALERTS
    // ==============================================================
    // Flash messages automatically disappear after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // ==============================================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ==============================================================
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                e.preventDefault();
                const target = document.querySelector(targetId);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ==============================================================
    // ANIMATED COUNTER (Stats Section)
    // ==============================================================
    function animateCounter(element, target, duration) {
        let start = 0;
        const increment = target / (duration / 16); // ~60fps
        const timer = setInterval(function() {
            start += increment;
            if (start >= target) {
                element.textContent = target.toLocaleString() + '+';
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(start).toLocaleString() + '+';
            }
        }, 16);
    }

    // Intersection Observer for counter animation
    const counters = document.querySelectorAll('.stat-counter');
    if (counters.length > 0) {
        const counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.getAttribute('data-target')) || 0;
                    animateCounter(entry.target, target, 2000);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(function(counter) {
            counterObserver.observe(counter);
        });
    }

    // ==============================================================
    // SCROLL REVEAL ANIMATION
    // ==============================================================
    // Fade in elements as they appear in viewport
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    if (revealElements.length > 0) {
        const revealObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealElements.forEach(function(el) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            revealObserver.observe(el);
        });
    }

    // Add revealed class styles
    const style = document.createElement('style');
    style.textContent = '.revealed { opacity: 1 !important; transform: translateY(0) !important; }';
    document.head.appendChild(style);

    // ==============================================================
    // FORM VALIDATION (Client-side)
    // ==============================================================
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // ==============================================================
    // PHONE NUMBER FORMATTING
    // ==============================================================
    const phoneInputs = document.querySelectorAll('input[id*="phone"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            // Allow only digits, spaces, dashes, and plus sign
            this.value = this.value.replace(/[^0-9+\-\s]/g, '');
        });
    });

    // ==============================================================
    // PASSWORD STRENGTH INDICATOR
    // ==============================================================
    const passwordInput = document.getElementById('signup-password1');
    if (passwordInput) {
        // Create strength indicator
        const strengthBar = document.createElement('div');
        strengthBar.className = 'password-strength mt-1';
        strengthBar.innerHTML = '<div class="strength-bar"><div class="strength-fill"></div></div><small class="strength-text text-muted"></small>';
        passwordInput.parentNode.appendChild(strengthBar);

        // Add styles
        const pwStyle = document.createElement('style');
        pwStyle.textContent = `
            .strength-bar { height: 4px; background: #e0e0e0; border-radius: 4px; overflow: hidden; }
            .strength-fill { height: 100%; border-radius: 4px; transition: width 0.3s ease, background 0.3s ease; width: 0; }
        `;
        document.head.appendChild(pwStyle);

        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            if (password.length >= 8) strength++;
            if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
            if (/\d/.test(password)) strength++;
            if (/[^a-zA-Z0-9]/.test(password)) strength++;

            const fill = strengthBar.querySelector('.strength-fill');
            const text = strengthBar.querySelector('.strength-text');

            const levels = [
                { width: '0%', color: '#e0e0e0', label: '' },
                { width: '25%', color: '#e94560', label: 'Weak' },
                { width: '50%', color: '#e67e22', label: 'Fair' },
                { width: '75%', color: '#f5c518', label: 'Good' },
                { width: '100%', color: '#2ecc71', label: 'Strong' },
            ];

            fill.style.width = levels[strength].width;
            fill.style.background = levels[strength].color;
            text.textContent = levels[strength].label;
            text.style.color = levels[strength].color;
        });
    }

    // ==============================================================
    // FILE INPUT PREVIEW
    // ==============================================================
    const photoInput = document.getElementById('reg-photo') || document.getElementById('edit-photo');
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file type
                if (!file.type.startsWith('image/')) {
                    alert('Please select an image file.');
                    this.value = '';
                    return;
                }
                // Validate size (2 MB)
                if (file.size > 2 * 1024 * 1024) {
                    alert('Image must be less than 2 MB.');
                    this.value = '';
                    return;
                }
            }
        });
    }

    const resumeInput = document.getElementById('reg-resume') || document.getElementById('edit-resume');
    if (resumeInput) {
        resumeInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate size (5 MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('Resume must be less than 5 MB.');
                    this.value = '';
                    return;
                }
            }
        });
    }

    // ==============================================================
    // CONFIRM DELETE DIALOGS
    // ==============================================================
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // ==============================================================
    // ACTIVE NAV LINK HIGHLIGHTING
    // ==============================================================
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-main .nav-link').forEach(function(link) {
        const href = link.getAttribute('href');
        if (href && href !== '/' && currentPath.startsWith(href)) {
            link.classList.add('active');
        }
    });

    // ==============================================================
    // TOOLTIP INITIALIZATION
    // ==============================================================
    const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipElements.forEach(function(el) {
        new bootstrap.Tooltip(el);
    });

    // ==============================================================
    // SELECT ALL CHECKBOX (for volunteer assignment)
    // ==============================================================
    const selectAllCheckbox = document.getElementById('selectAll');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('input[name="volunteers"]');
            checkboxes.forEach(function(cb) {
                cb.checked = selectAllCheckbox.checked;
            });
        });
    }

    console.log('🌟 NayePankh Foundation - System Loaded Successfully!');
});
