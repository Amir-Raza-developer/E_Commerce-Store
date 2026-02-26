# ShopHub - Full E-Commerce Store

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```
   Then go to Django admin → Users → set role to "admin"

4. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## User Roles
- **Buyer** — can browse, add to cart, checkout, manage wishlist
- **Seller** — can add/edit/delete products, manage orders
- **Admin** — full access to everything

## URLs
| URL | Page |
|-----|------|
| `/` | Home |
| `/shop/` | Shop (browse all products) |
| `/product/<id>/` | Product detail |
| `/cart/` | Shopping cart |
| `/checkout/` | Checkout |
| `/order-success/<id>/` | Order confirmation |
| `/login/` | Login |
| `/register/` | Register |
| `/profile/` | User profile + order history |
| `/product-management/` | Seller: manage products |
| `/order-management/` | Seller/Admin: manage orders |
| `/admin/` | Django admin panel |
