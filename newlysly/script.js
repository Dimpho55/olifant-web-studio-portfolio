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

// --- Homepage slideshow ---
(function(){
    let slideIndex = 0;
    let slides = [];
    let dots = [];
    let timer = null;
    const interval = 4000;

    function showSlide(n){
        if (!slides.length) return;
        slides.forEach((s, i) => s.classList.toggle('active', i === n));
        dots.forEach((d, i) => d.classList.toggle('active', i === n));
        slideIndex = n;
    }

    function next(){ showSlide((slideIndex + 1) % slides.length); }
    function prev(){ showSlide((slideIndex - 1 + slides.length) % slides.length); }

    function start(){ stop(); timer = setInterval(next, interval); }
    function stop(){ if (timer) { clearInterval(timer); timer = null; } }

    document.addEventListener('DOMContentLoaded', function(){
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

        // pause on hover
        wrap.addEventListener('mouseenter', stop);
        wrap.addEventListener('mouseleave', start);

        showSlide(0);
        start();
    });
})();
