from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from products.models import Product, Category
from Seller.models import Order, OrderItem
from .models import Wishlist


# ── Home Page ──────────────────────────────────────────────
def home_view(request):
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories        = Category.objects.all()
    return render(request, 'index.html', {
        'products':   featured_products,
        'categories': categories,
    })


# ── Shop Page ──────────────────────────────────────────────
def shop_view(request):
    products   = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category__id=category_id)

    # Search
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    # Sort
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    return render(request, 'shop.html', {
        'products':   products,
        'categories': categories,
    })


# ── Product Detail ─────────────────────────────────────────
def product_detail_view(request, pk):
    product  = get_object_or_404(Product, pk=pk, is_active=True)
    related  = Product.objects.filter(category=product.category, is_active=True).exclude(pk=pk)[:4]
    return render(request, 'product.html', {
        'product': product,
        'related': related,
    })


# ── Add to Cart ────────────────────────────────────────────
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    cart = request.session.get('cart', {})
    key  = str(pk)

    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {
            'name':     product.name,
            'price':    str(product.price),
            'image':    product.image.url if product.image else '',
            'quantity': 1,
        }

    request.session['cart'] = cart
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('cart')


# ── Remove from Cart ───────────────────────────────────────
def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect('cart')


# ── Update Cart Quantity ───────────────────────────────────
def update_cart(request, pk):
    if request.method == 'POST':
        cart     = request.session.get('cart', {})
        key      = str(pk)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0 and key in cart:
            cart[key]['quantity'] = quantity
        elif quantity <= 0:
            cart.pop(key, None)

        request.session['cart'] = cart
    return redirect('cart')


# ── Cart Page ──────────────────────────────────────────────
def cart_view(request):
    cart     = request.session.get('cart', {})
    subtotal = sum(float(item['price']) * item['quantity'] for item in cart.values())
    shipping = 10.00 if subtotal > 0 else 0
    tax      = round(subtotal * 0.05, 2)
    total    = round(subtotal + shipping + tax, 2)

    return render(request, 'cart.html', {
        'cart':     cart,
        'subtotal': round(subtotal, 2),
        'shipping': shipping,
        'tax':      tax,
        'total':    total,
    })


# ── Checkout Page ──────────────────────────────────────────
@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    subtotal = sum(float(item['price']) * item['quantity'] for item in cart.values())
    shipping = 10.00
    tax      = round(subtotal * 0.05, 2)
    total    = round(subtotal + shipping + tax, 2)

    if request.method == 'POST':
        # Create the Order
        order = Order.objects.create(
            buyer          = request.user,
            total          = total,
            payment_method = request.POST.get('payment', 'cod'),
            full_name      = f"{request.POST.get('first_name')} {request.POST.get('last_name')}",
            email          = request.POST.get('email'),
            phone          = request.POST.get('phone'),
            address        = request.POST.get('address'),
            city           = request.POST.get('city'),
            state          = request.POST.get('state'),
            zip_code       = request.POST.get('zip_code'),
        )

        # Create OrderItems and reduce stock
        for pk, item in cart.items():
            product = get_object_or_404(Product, pk=pk)
            OrderItem.objects.create(
                order    = order,
                product  = product,
                quantity = item['quantity'],
                price    = item['price'],
            )
            # Reduce stock
            product.stock -= item['quantity']
            product.save()

        # Clear cart
        request.session['cart'] = {}
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart':     cart,
        'subtotal': round(subtotal, 2),
        'shipping': shipping,
        'tax':      tax,
        'total':    total,
        'user':     request.user,
    })


# ── Order Success Page ─────────────────────────────────────
@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, 'order-success.html', {'order': order})


# ── Wishlist ───────────────────────────────────────────────
@login_required
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        obj.delete()
        messages.info(request, f'"{product.name}" removed from wishlist.')
    else:
        messages.success(request, f'"{product.name}" added to wishlist!')

    return redirect('product_detail', pk=pk)