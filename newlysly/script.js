function addToCart(id, name, price, imagePath) {
    // Find the product card that called this (to read size and qty inputs nearby)
    // If invoked from inline onclick, use event target fallback
    let size = 'One Size';
    let qty = 1;
    try {
        // locate the button element by searching all buttons with matching onclick containing id
        const buttons = Array.from(document.querySelectorAll('button'));
        let btn = buttons.find(b => b.getAttribute('onclick') && b.getAttribute('onclick').includes(id));
        if (!btn && window.event && window.event.target) btn = window.event.target;
        if (btn) {
            const card = btn.closest('.product');
            if (card) {
                const s = card.querySelector('.size-select');
                const q = card.querySelector('.qty');
                if (s) size = s.value;
                if (q) qty = parseInt(q.value) || 1;
            }
        }
    } catch (e) {
        // ignore
    }

    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    cart.push({ id, name, price: Number(price), size, qty, image: imagePath });
    localStorage.setItem('cart', JSON.stringify(cart));

    alert(name + ' added to cart!');

    // update cart count if present
    const countEl = document.getElementById('cart-count');
    if (countEl) {
        const totalItems = cart.reduce((s, it) => s + (it.qty || 1), 0);
        countEl.innerText = totalItems;
    }
}

// small helper to compute 10% sale price if needed
function salePrice(orig) {
    return Math.round((orig * 0.9) * 100) / 100;
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

// MOBILE MENU TOGGLE
document.addEventListener('DOMContentLoaded', function(){
    const navUl = document.querySelector('.navbar ul');
    const navbarElem = document.querySelector('.navbar');
    
    // Create hamburger menu for mobile
    if (window.innerWidth <= 768 && !document.querySelector('.hamburger')) {
        const hamburger = document.createElement('button');
        hamburger.classList.add('hamburger');
        hamburger.innerHTML = '☰';
        hamburger.addEventListener('click', () => {
            navUl.classList.toggle('active');
        });
        navbarElem.appendChild(hamburger);
    }
    
    // Close menu when link is clicked
    document.querySelectorAll('.navbar a').forEach(link => {
        link.addEventListener('click', () => {
            navUl.classList.remove('active');
        });
    });

// --- Homepage slideshow ---
    let slideIndex = 0;
    let slides = [];
    let dots = [];
    let timer = null;
    let intervalMs = 4000;

    function showSlide(n){
        if (!slides.length) return;
        slides.forEach((s, i) => s.classList.toggle('active', i === n));
        dots.forEach((d, i) => d.classList.toggle('active', i === n));
        slideIndex = n;
    }

    function next(){ showSlide((slideIndex + 1) % slides.length); }
    function prev(){ showSlide((slideIndex - 1 + slides.length) % slides.length); }

    function start(){ stop(); if (!slides.length) return; timer = setInterval(next, intervalMs); }
    function stop(){ if (timer) { clearInterval(timer); timer = null; } }
    
        const wrap = document.getElementById('slideshow');
        if (!wrap) return;
        slides = Array.from(wrap.querySelectorAll('.slide'));

        const dotsWrap = document.getElementById('slideDots');
        slides.forEach((s, i) => {
            const b = document.createElement('button');
            b.addEventListener('click', () => { showSlide(i); start(); });
            dotsWrap.appendChild(b);
            dots.push(b);
        });

        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        if (prevBtn) prevBtn.addEventListener('click', () => { prev(); start(); });
        if (nextBtn) nextBtn.addEventListener('click', () => { next(); start(); });

        // speed selector
        const speedSelect = document.getElementById('slideSpeed');
        if (speedSelect) {
            intervalMs = parseInt(speedSelect.value, 10) || intervalMs;
            speedSelect.addEventListener('change', function(){
                intervalMs = parseInt(this.value, 10) || intervalMs;
                start();
            });
        }

        // pause on hover
        wrap.addEventListener('mouseenter', stop);
        wrap.addEventListener('mouseleave', start);

        // thumbnails (if present)
        const thumbsWrap = document.getElementById('slideThumbs');
        let thumbs = [];
        if (thumbsWrap) {
            thumbs = Array.from(thumbsWrap.querySelectorAll('button'));
            thumbs.forEach((t, i) => {
                t.addEventListener('click', () => { showSlide(i); start(); });
            });
        }

        // thumbnail image fade-in when loaded
        const thumbImgs = Array.from(document.querySelectorAll('.thumb-img'));
        thumbImgs.forEach(img => {
            if (img.complete) { img.classList.add('loaded'); }
            else img.addEventListener('load', () => img.classList.add('loaded'));
            img.addEventListener('error', () => img.classList.add('loaded'));
        });

        // touch-swipe support
        let touchStartX = 0;
        let touchEndX = 0;
        const threshold = 40; // px
        wrap.addEventListener('touchstart', (e) => { touchStartX = e.changedTouches[0].clientX; stop(); }, {passive:true});
        wrap.addEventListener('touchmove', (e) => { touchEndX = e.changedTouches[0].clientX; }, {passive:true});
        wrap.addEventListener('touchend', (e) => {
            touchEndX = touchEndX || e.changedTouches[0].clientX;
            const dx = touchStartX - touchEndX;
            if (Math.abs(dx) > threshold) {
                if (dx > 0) next(); else prev();
            }
            start();
            touchStartX = touchEndX = 0;
        });

        showSlide(0);
        start();
    }
});
