from flask import Flask, jsonify, request, session, abort
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app)
app.secret_key = 'replace-this-with-a-secure-key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Product catalog for NEWLY SLY
PRODUCTS = [
    {'id': 1, 'name': 'newlysly-tee-tyedye', 'price': 299, 'category': 'shirts', 'rating': 4.9},
    {'id': 2, 'name': 'newlysly-hoodie-orange', 'price': 499, 'category': 'hoodies', 'rating': 4.8},
    {'id': 3, 'name': 'newlysly-denim-black', 'price': 599, 'category': 'pants', 'rating': 4.5},
    {'id': 4, 'name': 'newlysly-hoodie-black', 'price': 799, 'category': 'shoes', 'rating': 4.9},
    {'id': 5, 'name': 'newlysly-beanie-black', 'price': 199, 'category': 'accessories', 'rating': 4.4},
    {'id': 6, 'name': 'newlysly-beanie-green', 'price': 249, 'category': 'accessories', 'rating': 4.7},
    {'id': 7, 'name': 'newlysly-sweatpants-purple', 'price': 449, 'category': 'bags', 'rating': 4.8},
    {'id': 8, 'name': 'newlysly-tee-white', 'price': 349, 'category': 'accessories', 'rating': 4.3}
]

# In-memory session cart management
@app.before_request
def ensure_cart():
    session.permanent = True
    if 'cart' not in session:
        session['cart'] = []

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({'data': PRODUCTS})

@app.route('/api/cart', methods=['GET'])
def get_cart():
    return jsonify({'cart': session.get('cart', [])})

@app.route('/api/cart', methods=['POST'])
def add_cart_item():
    data = request.json
    if not data or 'productId' not in data or 'quantity' not in data:
        abort(400, description='productId and quantity are required')

    product_id = int(data['productId'])
    quantity = int(data['quantity'])
    if quantity <= 0:
        abort(400, description='Quantity must be positive')

    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        abort(404, description='Product not found')

    cart = session.get('cart', [])
    existing = next((item for item in cart if item['id'] == product_id), None)
    if existing:
        existing['quantity'] += quantity
    else:
        cart.append({'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': quantity})

    session['cart'] = cart
    return jsonify({'cart': cart})

@app.route('/api/cart', methods=['PUT'])
def update_cart_item():
    data = request.json
    if not data or 'productId' not in data or 'quantity' not in data:
        abort(400, description='productId and quantity are required')

    product_id = int(data['productId'])
    quantity = int(data['quantity'])
    cart = session.get('cart', [])

    existing = next((item for item in cart if item['id'] == product_id), None)
    if not existing:
        abort(404, description='Cart item not found')

    if quantity <= 0:
        cart = [item for item in cart if item['id'] != product_id]
    else:
        existing['quantity'] = quantity

    session['cart'] = cart
    return jsonify({'cart': cart})

@app.route('/api/cart', methods=['DELETE'])
def delete_cart_item():
    data = request.json
    if not data or 'productId' not in data:
        abort(400, description='productId is required')

    product_id = int(data['productId'])
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return jsonify({'cart': cart})

@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    session['cart'] = []
    return jsonify({'cart': []})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
