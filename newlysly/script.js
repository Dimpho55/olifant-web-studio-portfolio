// NEWLY SLY E-Commerce Cart System

// Initialize cart from localStorage
let cart = JSON.parse(localStorage.getItem('newlysly-cart')) || [];

// Product Database
const products = [
    {
        id: 1,
        name: 'Urban Tee',
        price: 299,
        category: 'shirts',
        rating: '⭐⭐⭐⭐⭐ (21 reviews)',
        icon: '👕'
    },
    {
        id: 2,
        name: 'Street Hoodie',
        price: 499,
        category: 'hoodies',
        rating: '⭐⭐⭐⭐⭐ (18 reviews)',
        icon: '🧥'
    },
    {
        id: 3,
        name: 'Cargo Pants',
        price: 599,
        category: 'pants',
        rating: '⭐⭐⭐⭐ (15 reviews)',
        icon: '👖'
    },
    {
        id: 4,
        name: 'Sneaker High',
        price: 799,
        category: 'shoes',
        rating: '⭐⭐⭐⭐⭐ (32 reviews)',
        icon: '👟'
    },
    {
        id: 5,
        name: 'Bucket Hat',
        price: 199,
        category: 'accessories',
        rating: '⭐⭐⭐⭐ (12 reviews)',
        icon: '🎩'
    },
    {
        id: 6,
        name: 'Chain Necklace',
        price: 249,
        category: 'accessories',
        rating: '⭐⭐⭐⭐⭐ (8 reviews)',
        icon: '⛓️'
    },
    {
        id: 7,
        name: 'Backpack Pro',
        price: 449,
        category: 'bags',
        rating: '⭐⭐⭐⭐⭐ (24 reviews)',
        icon: '🎒'
    },
    {
        id: 8,
        name: 'Sunglasses',
        price: 349,
        category: 'accessories',
        rating: '⭐⭐⭐⭐ (10 reviews)',
        icon: '😎'
    }
];

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking on a link
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
            });
        });
    }

    // Initialize products on shop page
    if (document.getElementById('products-container')) {
        renderProducts();
    }

    // Initialize cart display on cart page
    if (document.querySelector('.cart-items')) {
        updateCartDisplay();
    }

    // Update cart count in navbar
    updateCartCount();
});

// Render products on shop page
function renderProducts(filter = 'all') {
    const container = document.getElementById('products-container');
    if (!container) return;

    container.innerHTML = '';

    let filteredProducts = products;
    if (filter !== 'all') {
        filteredProducts = products.filter(p => p.category === filter);
    }

    filteredProducts.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <div class="product-image">
                <i style="font-size: 3rem;">${product.icon}</i>
            </div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <p class="product-price">R ${product.price}</p>
                <p class="product-rating">${product.rating}</p>
                <button class="btn" onclick="addToCart(${product.id})">Add to Cart</button>
                <div class="quantity-selector" style="display: none;">
                    <button onclick="decreaseQuantity(${product.id})">-</button>
                    <input type="number" value="1" min="1" max="99" id="qty-${product.id}">
                    <button onclick="increaseQuantity(${product.id})">+</button>
                </div>
            </div>
        `;
        container.appendChild(productCard);
    });
}

// Add to cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const quantityInput = document.getElementById(`qty-${productId}`);
    const quantity = quantityInput ? parseInt(quantityInput.value) : 1;

    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            id: productId,
            name: product.name,
            price: product.price,
            quantity: quantity,
            icon: product.icon
        });
    }

    saveCart();
    updateCartCount();
    
    // Show notification
    showNotification(`${product.name} added to cart!`);
}

// Remove from cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    saveCart();
    updateCartDisplay();
    updateCartCount();
}

// Update item quantity
function updateQuantity(productId, quantity) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity = quantity;
        if (item.quantity <= 0) {
            removeFromCart(productId);
        } else {
            saveCart();
            updateCartDisplay();
        }
    }
}

// Save cart to localStorage
function saveCart() {
    localStorage.setItem('newlysly-cart', JSON.stringify(cart));
}

// Update cart count in navbar
function updateCartCount() {
    const cartCountElements = document.querySelectorAll('.cart-count');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    cartCountElements.forEach(element => {
        element.textContent = totalItems > 0 ? totalItems : '0';
    });
}

// Display cart items
function updateCartDisplay() {
    const cartItemsContainer = document.querySelector('.cart-items');
    const emptySectionContainer = document.querySelector('.cart-empty');

    if (!cartItemsContainer) return;

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '';
        if (emptySectionContainer) {
            emptySectionContainer.style.display = 'block';
        }
        const summaryContainer = document.querySelector('.cart-summary');
        if (summaryContainer) {
            summaryContainer.style.display = 'none';
        }
        return;
    }

    if (emptySectionContainer) {
        emptySectionContainer.style.display = 'none';
    }

    cartItemsContainer.innerHTML = '';
    let totalPrice = 0;

    cart.forEach(item => {
        totalPrice += item.price * item.quantity;
        const itemHTML = `
            <div class="cart-item">
                <div class="cart-item-image">${item.icon}</div>
                <div class="cart-item-details">
                    <h4>${item.name}</h4>
                    <p>R ${item.price}</p>
                </div>
                <div class="cart-item-quantity">
                    <button onclick="updateQuantity(${item.id}, ${item.quantity - 1})">−</button>
                    <input type="number" value="${item.quantity}" min="1" max="99" onchange="updateQuantity(${item.id}, this.value)">
                    <button onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                </div>
                <div class="cart-item-total">R ${(item.price * item.quantity).toLocaleString()}</div>
                <button class="cart-remove" onclick="removeFromCart(${item.id})">✕</button>
            </div>
        `;
        cartItemsContainer.innerHTML += itemHTML;
    });

    // Update cart summary
    const summaryContainer = document.querySelector('.cart-summary');
    if (summaryContainer) {
        summaryContainer.style.display = 'block';
        summaryContainer.innerHTML = `
            <div class="cart-summary-row">
                <span>Subtotal:</span>
                <span>R ${totalPrice.toLocaleString()}</span>
            </div>
            <div class="cart-summary-row">
                <span>Shipping:</span>
                <span>+ R 99</span>
            </div>
            <div class="cart-summary-row">
                <span>Tax (15%):</span>
                <span>R ${Math.round(totalPrice * 0.15).toLocaleString()}</span>
            </div>
            <div class="cart-summary-row total">
                <span>Total:</span>
                <span>R ${(totalPrice + 99 + Math.round(totalPrice * 0.15)).toLocaleString()}</span>
            </div>
            <button class="btn" style="margin-top: 20px; width: 100%;" onclick="window.location.href='checkout.html'">Proceed to Checkout</button>
        `;
    }
}

// Checkout - display order summary
function displayCheckoutSummary() {
    const summaryContainer = document.querySelector('.checkout-summary');
    if (!summaryContainer) return;

    let totalPrice = 0;
    let itemsHTML = '';

    cart.forEach(item => {
        totalPrice += item.price * item.quantity;
        itemsHTML += `
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid var(--accent-teal);">
                <span>${item.name} x${item.quantity}</span>
                <span>R ${(item.price * item.quantity).toLocaleString()}</span>
            </div>
        `;
    });

    const shipping = 99;
    const tax = Math.round(totalPrice * 0.15);
    const finalTotal = totalPrice + shipping + tax;

    summaryContainer.innerHTML = `
        <h3 style="margin-bottom: 20px; color: var(--accent-lime);">Order Summary</h3>
        ${itemsHTML}
        <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid var(--accent-lime);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span>Subtotal:</span>
                <span>R ${totalPrice.toLocaleString()}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span>Shipping:</span>
                <span>+ R ${shipping}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span>Tax (15%):</span>
                <span>R ${tax.toLocaleString()}</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 1.3rem; font-weight: bold; color: var(--accent-lime); margin-top: 15px;">
                <span>Total:</span>
                <span>R ${finalTotal.toLocaleString()}</span>
            </div>
        </div>
    `;
}

// Handle checkout form submission
function submitCheckout(event) {
    event.preventDefault();

    const name = document.getElementById('fullname').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const address = document.getElementById('address').value;

    if (!name || !email || !phone || !address) {
        alert('Please fill in all fields');
        return;
    }

    // Simulate order processing
    const orderNumber = 'ORD-' + Date.now();
    let orderItems = '';
    cart.forEach(item => {
        orderItems += `${item.name} x${item.quantity}, `;
    });

    const emailBody = `
Hello ${name},

Thank you for your order at NEWLY SLY!

Order Number: ${orderNumber}
Items: ${orderItems.slice(0, -2)}
Total: R ${calculateTotal().toLocaleString()}

Your order will be shipped to:
${address}

We'll contact you at ${phone} to confirm delivery.

Cheers,
NEWLY SLY Team
    `;

    // In production, this would send to a backend server
    const mailtoLink = `mailto:${email}?subject=Order Confirmation - ${orderNumber}&body=${encodeURIComponent(emailBody)}`;
    window.location.href = mailtoLink;

    // Clear cart after successful checkout (in demo)
    setTimeout(() => {
        cart = [];
        saveCart();
        updateCartCount();
        alert('Order confirmed! Check your email for details.');
        window.location.href = 'index.html';
    }, 1000);
}

// Calculate total price
function calculateTotal() {
    let total = 0;
    cart.forEach(item => {
        total += item.price * item.quantity;
    });
    const shipping = 99;
    const tax = Math.round(total * 0.15);
    return total + shipping + tax;
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: linear-gradient(135deg, #35b67d, #0f7173);
        color: white;
        padding: 15px 25px;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 9999;
        animation: slideInDown 0.5s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.5s ease';
        setTimeout(() => notification.remove(), 500);
    }, 2000);
}

// Filter products by category
function filterProducts(category) {
    renderProducts(category);
    updateActiveFilter(category);
}

// Update active filter button
function updateActiveFilter(category) {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-filter="${category}"]`).classList.add('active');
}

// Increase quantity in product card
function increaseQuantity(productId) {
    const input = document.getElementById(`qty-${productId}`);
    input.value = parseInt(input.value) + 1;
}

// Decrease quantity in product card
function decreaseQuantity(productId) {
    const input = document.getElementById(`qty-${productId}`);
    if (parseInt(input.value) > 1) {
        input.value = parseInt(input.value) - 1;
    }
}
