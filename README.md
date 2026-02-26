# E-commerce Platform

A complete Flask-based e-commerce platform with product browsing, shopping cart, checkout, and order confirmation.

## Features

- ✅ User Authentication (Login & Signup)
- ✅ Product Browsing (14+ products)
- ✅ Shopping Cart Management
- ✅ Checkout Process
- ✅ Order Confirmation
- ✅ Email Validation
- ✅ Responsive Design

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/HackToHire-HYD01/Mehdi_Monis_UC31_repo.git
cd Ecom_platform
```

2. **Create virtual environment**
```bash
python -m venv myenvEcom
```

3. **Activate virtual environment**
```bash
# On Windows
myenvEcom\Scripts\activate

# On macOS/Linux
source myenvEcom/bin/activate
```

4. **Install dependencies**
```bash
pip install flask werkzeug
```

5. **Set environment variables** (Optional - for production)
```bash
# Create .env file with:
ECOM_USERNAME=Monis
ECOM_PASSWORD_HASH=hashed_password
```

## Running the Application

```bash
python app.py
```

The application will run on `http://127.0.0.1:5000`

## Demo Credentials

**Login Email:** `monis@example.com`  
**Password:** `Monis@123`

## Project Structure

```
Ecom_platform/
├── app.py                 # Main Flask application
├── services/
│   └── ecom_service.py   # Business logic for cart and products
├── templates/
│   ├── index.html        # Login/Signup page
│   ├── products.html     # Product listing
│   ├── cart.html         # Shopping cart
│   ├── checkout.html     # Checkout form
│   ├── order_confirmation.html # Order confirmation
│   └── show_product.html # Product details
├── static/               # Static assets (CSS, JS, images)
├── data/
│   └── product_catalog.json # Product data
└── .env                  # Environment variables
```

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /signup` - User registration
- `GET /logout` - User logout

### Products
- `GET /` - Home page
- `GET /products` - Browse all products
- `GET /products/<id>` - View product details

### Cart
- `POST /api/cart/add` - Add product to cart
- `POST /api/cart/remove` - Remove product from cart
- `GET /cart` - View shopping cart

### Checkout
- `GET /checkout` - Checkout form
- `POST /checkout` - Process checkout
- `GET /order-confirmation` - Order confirmation page

### Utilities
- `POST /api/validate-email` - Email validation API

## Product Catalog

The platform includes 14 laptop products with specifications:
- HP Pavilion, DELL Inspiron, Lenovo ThinkBook
- ASUS VivoBook, Apple MacBook Air M2, Samsung Galaxy Book
- And more...

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** JSON (product catalog)
- **Session Management:** Flask Sessions

## Future Enhancements

- Database integration (PostgreSQL)
- Payment gateway integration
- User profiles and order history
- Product search and filtering
- Admin dashboard
- Email notifications

## Author

Mehdi Monis - UC31 Hackathon Project

## License

This project is open source and available under the MIT License.
