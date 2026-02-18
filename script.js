// SLIDESHOW FUNCTIONALITY
let slideIndex = 1;
let slideTimer;

function showSlides(n) {
    const slides = document.getElementsByClassName("slide");
    const indicators = document.getElementsByClassName("indicator");
    
    if (n > slides.length) { slideIndex = 1; }
    if (n < 1) { slideIndex = slides.length; }
    
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (let i = 0; i < indicators.length; i++) {
        indicators[i].classList.remove("active");
    }
    
    slides[slideIndex - 1].style.display = "block";
    indicators[slideIndex - 1].classList.add("active");
}

function currentSlide(n) {
    clearTimeout(slideTimer);
    showSlides(slideIndex = n);
    autoSlides();
}

function autoSlides() {
    slideTimer = setTimeout(() => {
        slideIndex++;
        showSlides(slideIndex);
        autoSlides();
    }, 5000); // Change slide every 5 seconds
}

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

// MOBILE MENU TOGGLE (for responsive nav)
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelector('.nav-links');
    const navbar = document.querySelector('.navbar');
    
    // Create hamburger menu for mobile
    if (window.innerWidth <= 768 && !document.querySelector('.hamburger')) {
        const hamburger = document.createElement('button');
        hamburger.classList.add('hamburger');
        hamburger.innerHTML = '☰';
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
        navbar.appendChild(hamburger);
    }
    
    // Close menu when link is clicked
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });
});

// START SLIDESHOW ON PAGE LOAD
document.addEventListener('DOMContentLoaded', () => {
    showSlides(slideIndex);
    autoSlides();
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

document.querySelectorAll(".service-card, .portfolio-card, .about, .stat-box")
    .forEach(el => {
        el.classList.add("hidden");
        observer.observe(el);
    });

// FORM SUBMISSION
const contactForm = document.querySelector(".contact-form");
if (contactForm) {
    contactForm.addEventListener("submit", (e) => {
        e.preventDefault();
        alert("Thank you for your message! We'll get back to you soon.");
        contactForm.reset();
    });
}
