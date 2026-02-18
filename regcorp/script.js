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