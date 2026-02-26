from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from products.models import Product, Category
from .models import Order, OrderItem
from .forms import ProductForm


def seller_required(view_func):
    """Decorator — only sellers and admins can access."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['seller', 'admin']:
            messages.error(request, 'Access denied. Seller account required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ── Product Management ─────────────────────────────────────
@seller_required
def product_management(request):
    if request.user.role == 'admin':
        products = Product.objects.all().order_by('-created_at')
    else:
        products = Product.objects.filter(seller=request.user).order_by('-created_at')

    categories = Category.objects.all()

    # Search
    search = request.GET.get('search', '')
    if search:
        products = products.filter(name__icontains=search)

    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category__id=category_id)

    # Add product
    if request.method == 'POST' and 'add_product' in request.POST:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('product_management')
        else:
            messages.error(request, 'Please fix the errors in the form.')
    else:
        form = ProductForm()

    return render(request, 'product-management.html', {
        'products':    products,
        'categories':  categories,
        'form':        form,
        'search':      search,
        'category_id': category_id,
    })


# ── Edit Product ───────────────────────────────────────────
@seller_required
def edit_product(request, pk):
    if request.user.role == 'admin':
        product = get_object_or_404(Product, pk=pk)
    else:
        product = get_object_or_404(Product, pk=pk, seller=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('product_management')
        else:
            messages.error(request, 'Please fix the errors in the form.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit-product.html', {'form': form, 'product': product})


# ── Delete Product ─────────────────────────────────────────
@seller_required
def delete_product(request, pk):
    if request.user.role == 'admin':
        product = get_object_or_404(Product, pk=pk)
    else:
        product = get_object_or_404(Product, pk=pk, seller=request.user)

    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted successfully!')

    return redirect('product_management')


# ── Order Management ───────────────────────────────────────
@seller_required
def order_management(request):
    if request.user.role == 'admin':
        orders = Order.objects.all().order_by('-created_at')
    else:
        # Seller sees only orders that contain their products
        orders = Order.objects.filter(
            items__product__seller=request.user
        ).distinct().order_by('-created_at')

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'order-management.html', {
        'orders':        orders,
        'status_filter': status_filter,
    })


# ── Order Detail ───────────────────────────────────────────
@seller_required
def order_detail(request, pk):
    if request.user.role == 'admin':
        order = get_object_or_404(Order, pk=pk)
    else:
        order = get_object_or_404(
            Order,
            pk=pk,
            items__product__seller=request.user
        )

    items = order.items.all()
    return render(request, 'order-detail.html', {'order': order, 'items': items})


# ── Update Order Status ────────────────────────────────────
@seller_required
def update_order_status(request, pk):
    if request.user.role == 'admin':
        order = get_object_or_404(Order, pk=pk)
    else:
        order = get_object_or_404(
            Order,
            pk=pk,
            items__product__seller=request.user
        )

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to "{new_status}".')

    return redirect('order_management')
