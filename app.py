import json
import os
import uuid
import re
from flask import Flask, render_template, abort, request, jsonify, session, redirect, url_for
from services.ecom_service import add_to_cart, remove_from_cart, get_cart, get_cart_total
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400

# User credentials from environment variables
VALID_USERNAME = os.getenv('ECOM_USERNAME', 'Monis')
VALID_PASSWORD_HASH = os.getenv('ECOM_PASSWORD_HASH', generate_password_hash('Monis@123'))

# Load product catalog from JSON file
def load_product_catalog():
    try:
        catalog_path = os.path.join(os.path.dirname(__file__), 'data', 'product_catalog.json')
        print(f"Loading products from: {catalog_path}")
        with open(catalog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle both nested structure ({"products": [...]}) and flat array
            products = data.get('products') if isinstance(data, dict) else data
            print(f"Loaded {len(products) if products else 0} products")
            return products
    except Exception as e:
        print(f"Error loading product catalog: {e}")
        return None

product_catalog = load_product_catalog()

def get_user_id():
    """Get or create user session ID."""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session.permanent = True
    return session['user_id']

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Simple authentication: check against hardcoded credentials
        if email and password:
            # For demo: accept Monis@example.com with password "Monis@123"
            if email.lower() == 'monis@example.com' and password == 'Monis@123':
                session['logged_in'] = True
                session['username'] = 'Monis'
                session.permanent = True
                return redirect(url_for('browse_products'))
            else:
                return render_template('index.html', error='Invalid email or password')
        else:
            return render_template('index.html', error='Please enter email and password')
    
    return render_template('index.html')

@app.route("/signup", methods=["POST"])
def signup():
    """Handle user signup."""
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # For demo: allow signup but store in session
    if name and email and password:
        if len(password) < 6:
            return render_template('index.html', error='Password must be at least 6 characters')
        
        # Store user in session for demo purposes
        session['logged_in'] = True
        session['username'] = name
        session['email'] = email
        session.permanent = True
        return redirect(url_for('browse_products'))
    else:
        return render_template('index.html', error='Please fill all fields')

@app.route("/logout")
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for('home'))

@app.route("/")
def home():
    # Render the index template with product_catalog from data.py
    return render_template("index.html")

@app.route("/products")
def browse_products():
    # Get search query from request
    search_query = request.args.get('search', '').strip().lower()
    
    # Load products from catalog or use empty list
    products = product_catalog if product_catalog else []
    
    # Filter products by search query if provided
    if search_query:
        products = [
            p for p in products
            if search_query in p.get('name', '').lower() or
               search_query in p.get('other_details', {}).get('Brand', '').lower()
        ]
    
    username = session.get('username', 'Guest')
    return render_template("products.html", products=products, username=username, search_query=search_query)

@app.route("/products/<int:product_id>", methods=["GET"])
def show_product_details(product_id):
    # Load fresh product catalog to ensure we have products
    products = load_product_catalog() or []
    product = next((p for p in products if int(p.get("productId", -1)) == product_id), None)
    if not product:
        abort(404)
    return render_template("show_product.html", product=product)

@app.route("/api/cart/add", methods=["POST"])
def api_add_to_cart():
    """API endpoint to add product to cart."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid request'}), 400
        
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if not product_id or quantity < 1:
            return jsonify({'success': False, 'message': 'Invalid product_id or quantity'}), 400
        
        user_id = get_user_id()
        result = add_to_cart(user_id, int(product_id), quantity)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        print(f"Error in api_add_to_cart: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/api/cart/remove", methods=["POST"])
def api_remove_from_cart():
    """API endpoint to remove product from cart."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid request'}), 400
        
        product_id = data.get('product_id')
        if not product_id:
            return jsonify({'success': False, 'message': 'Invalid product_id'}), 400
        
        user_id = get_user_id()
        result = remove_from_cart(user_id, int(product_id))
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        print(f"Error in api_remove_from_cart: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/cart")
def view_cart():
    """Display user's cart."""
    user_id = get_user_id()
    cart = get_cart(user_id)
    total = get_cart_total(user_id)
    return render_template("cart.html", cart=cart, total=total)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    """Handle checkout process."""
    user_id = get_user_id()
    cart = get_cart(user_id)
    
    if not cart:
        return redirect(url_for('browse_products'))
    
    if request.method == "POST":
        # Collect form data
        customer_data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'zip_code': request.form.get('zip_code'),
            'payment_method': request.form.get('payment_method')
        }
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'payment_method']
        if all(customer_data.get(field) for field in required_fields):
            # Store order in session
            session['order'] = {
                'customer': customer_data,
                'cart': cart,
                'total': get_cart_total(user_id),
                'order_id': str(uuid.uuid4())
            }
            return redirect(url_for('order_confirmation'))
        else:
            return render_template('checkout.html', cart=cart, total=get_cart_total(user_id), error='Please fill all required fields')
    
    total = get_cart_total(user_id)
    return render_template('checkout.html', cart=cart, total=total)

@app.route("/order-confirmation")
def order_confirmation():
    """Display order confirmation."""
    if 'order' not in session:
        return redirect(url_for('browse_products'))
    
    order = session['order']
    return render_template('order_confirmation.html', order=order)

@app.route("/api/validate-email", methods=["POST"])
def validate_email():
    """Validate email format."""
    data = request.get_json()
    email = data.get('email', '')
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = re.match(email_pattern, email) is not None
    return jsonify({'valid': is_valid})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
