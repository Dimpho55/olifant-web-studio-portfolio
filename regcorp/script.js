// HIDE-ON-SCROLL NAVBAR
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
    if (currentScroll > lastScrollTop && currentScroll > 100) {
        navbar.classList.add('hide-navbar');
    } else {
        navbar.classList.remove('hide-navbar');
    }
    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
});

// MOBILE MENU TOGGLE
document.addEventListener('DOMContentLoaded', function(){
    const navLinks = document.querySelector('.navbar .nav-links');
    const navBar = document.querySelector('.navbar');
    
    // Create hamburger menu for mobile
    if (window.innerWidth <= 768 && !document.querySelector('.hamburger')) {
        const hamburger = document.createElement('button');
        hamburger.classList.add('hamburger');
        hamburger.innerHTML = '☰';
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
        navBar.appendChild(hamburger);
    }
    
    // Close menu when link is clicked
    document.querySelectorAll('.navbar a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });
});

// SMOOTH SCROLL
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
        e.preventDefault();
        const targetId = this.getAttribute("href");
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({ 
                behavior: "smooth",
                block: "start"
            });
        }
    });
});

// FADE-IN ANIMATION ON SCROLL
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });
}, {
    threshold: 0.1
});

document.querySelectorAll(".overview-item, .service-card, .vision-box, .mission-box, .contact-person-card, .contact-address-card")
    .forEach(el => {
        el.classList.add("hidden");
        observer.observe(el);
    });

// FORM SUBMISSION
const contactForm = document.querySelector(".contact-form");
if (contactForm) {
    contactForm.addEventListener("submit", (e) => {
        e.preventDefault();
        alert("Thank you for your inquiry! REGCORP will contact you shortly.");
        contactForm.reset();
    });
}