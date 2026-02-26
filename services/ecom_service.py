import json
import os
import psycopg2
from psycopg2 import sql

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ecom_db',
    'user': 'postgres',
    'password': 'password',
    'port': 5432
}

# In-memory cart storage (for demo purposes)
user_carts = {}

def load_product_catalog():
    """Load product catalog from JSON file."""
    try:
        catalog_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'product_catalog.json')
        with open(catalog_path, 'r') as f:
            data = json.load(f)
            return data.get('products') if isinstance(data, dict) else data
    except Exception as e:
        print(f"Error loading product catalog: {e}")
        return []

def get_all_products():
    """Retrieve all products from catalog."""
    return load_product_catalog()

def get_product_by_id(product_id):
    """Retrieve a specific product by ID."""
    products = load_product_catalog()
    return next((p for p in products if int(p.get("productId", -1)) == product_id), None)

def search_products(keyword):
    """Search products by name or other details."""
    products = load_product_catalog()
    keyword_lower = keyword.lower()
    return [p for p in products if keyword_lower in p.get('name', '').lower()]

def get_products_by_brand(brand):
    """Filter products by brand."""
    products = load_product_catalog()
    return [p for p in products if p.get('other_details', {}).get('Brand', '').lower() == brand.lower()]

def add_to_cart(user_id, product_id, quantity=1):
    """Add a product to user's cart."""
    try:
        product = get_product_by_id(product_id)
        if not product:
            return {'success': False, 'message': 'Product not found'}
        
        if user_id not in user_carts:
            user_carts[user_id] = []
        
        # Check if product already in cart
        existing_item = next((item for item in user_carts[user_id] if item['productId'] == product_id), None)
        
        if existing_item:
            existing_item['quantity'] += quantity
            message = f"Updated {product.get('name')} quantity in cart"
        else:
            cart_item = {
                'productId': product_id,
                'name': product.get('name'),
                'price': product.get('price'),
                'quantity': quantity,
                'other_details': product.get('other_details', {})
            }
            user_carts[user_id].append(cart_item)
            message = f"Added {product.get('name')} to cart"
        
        return {'success': True, 'message': message, 'cart_count': len(user_carts[user_id])}
    except Exception as e:
        print(f"Error in add_to_cart: {e}")
        return {'success': False, 'message': f'Error: {str(e)}'}

def remove_from_cart(user_id, product_id):
    """Remove a product from user's cart."""
    if user_id not in user_carts:
        return {'success': False, 'message': 'Cart not found'}
    
    user_carts[user_id] = [item for item in user_carts[user_id] if item['productId'] != product_id]
    return {'success': True, 'message': 'Product removed from cart', 'cart_count': len(user_carts[user_id])}

def get_cart(user_id):
    """Retrieve user's cart."""
    return user_carts.get(user_id, [])

def get_cart_total(user_id):
    """Calculate cart total."""
    cart = get_cart(user_id)
    return sum(item['price'] * item['quantity'] for item in cart)

def clear_cart(user_id):
    """Clear user's cart."""
    if user_id in user_carts:
        user_carts[user_id] = []
    return {'success': True, 'message': 'Cart cleared'}

def connect_to_db():
    """Establish database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None

def close_db_connection(conn):
    """Close database connection."""
    if conn:
        conn.close()

