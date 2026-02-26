// ==================================
// REGCORP PTY LTD - MAIN JS
// ==================================

document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    initFormSubmission();
    initScrollEffects();
});

// Mobile Menu Toggle
function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });

        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
    }
}

// Form Submission Handler
function initFormSubmission() {
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            console.log('Form submitted:', data);
            
            const messageEl = document.getElementById('formMessage');
            messageEl.textContent = 'Thank you for contacting REGCORP PTY LTD. We will get back to you shortly.';
            messageEl.classList.add('success');
            messageEl.classList.remove('error');
            
            form.reset();
            
            setTimeout(() => {
                messageEl.classList.remove('success');
            }, 5000);
        });
    }
}

// Scroll Effects
function initScrollEffects() {
    const cards = document.querySelectorAll('.overview-card, .service-box, .service-detail');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease-out';
        observer.observe(card);
    });
}

// Page scroll detection
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 5px 20px rgba(212, 175, 55, 0.1)';
    } else {
        navbar.style.boxShadow = 'none';
    }
});
