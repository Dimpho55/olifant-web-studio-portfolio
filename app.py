from flask import Flask, jsonify, request, session, abort
from flask_cors import CORS
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

@app.route('/api/contact', methods=['POST'])
def contact_form():
    data = request.json
    if not data:
        abort(400, description='No data provided')

    # Check if this is a NEWLY SLY contact form or main site form
    is_newlysly = 'subject' in data

    if is_newlysly:
        # NEWLY SLY contact form validation
        required_fields = ['firstName', 'lastName', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field].strip():
                abort(400, description=f'{field} is required')

        # Create NEWLY SLY email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"NEWLY SLY Contact - {data['subject']}"

        body = f"""
New contact form submission from NEWLY SLY website:

Name: {data['firstName']} {data['lastName']}
Email: {data['email']}
Subject: {data['subject']}
Order Number: {data.get('orderNumber', 'Not provided')}

Message:
{data['message']}
"""
    else:
        # Main site contact form validation
        required_fields = ['firstName', 'lastName', 'email', 'projectType', 'message']
        for field in required_fields:
            if field not in data or not data[field].strip():
                abort(400, description=f'{field} is required')

        # Create main site email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"Olifant Web Studio Contact - {data['projectType']}"

        body = f"""
New contact form submission from Olifant Web Studio website:

Name: {data['firstName']} {data['lastName']}
Email: {data['email']}
Company: {data.get('company', 'Not provided')}
Project Type: {data['projectType']}
Budget: {data.get('budget', 'Not specified')}

Message:
{data['message']}
"""

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return jsonify({'success': True, 'message': 'Email sent successfully'})
    except Exception as e:
        print(f"Email error: {e}")
        return jsonify({'success': False, 'message': 'Failed to send email'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
