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
