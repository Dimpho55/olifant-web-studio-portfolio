// Slideshow functionality
let slideIndex = 0;

function showSlide() {
    const slides = document.querySelectorAll('.slide');
    if (slideIndex >= slides.length) {
        slideIndex = 0;
    }
    slides.forEach((slide, index) => {
        slide.classList.remove('fade');
        if (index === slideIndex) {
            slide.classList.add('fade');
        }
    });
    slideIndex++;
    setTimeout(showSlide, 5000); // Change slide every 5 seconds
}

// Start slideshow on page load
window.addEventListener('load', () => {
    showSlide();
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            target.scrollIntoView({ behavior: "smooth" });
        }
    });
});

// Fade-in animation on scroll
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if(entry.isIntersecting){
            entry.target.classList.add("show");
        }
    });
});

document.querySelectorAll(".service-card, .portfolio-card, .about-content")
.forEach(el => {
    el.classList.add("hidden");
    observer.observe(el);
});

