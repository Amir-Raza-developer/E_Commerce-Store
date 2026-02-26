from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to ShopHub, {user.first_name}!')
            if user.role == 'seller':
                return redirect('product_management')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            if user.role == 'admin':
                return redirect('order_management')
            elif user.role == 'seller':
                return redirect('product_management')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm(request)
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request):
    from Seller.models import Order
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form, 'orders': orders})


@login_required
def order_management_view(request):
    if request.user.role not in ['admin', 'seller']:
        messages.error(request, 'Access denied.')
        return redirect('home')

    from Seller.models import Order
    if request.user.role == 'admin':
        orders = Order.objects.all().order_by('-created_at')
    else:
        orders = Order.objects.filter(
            items__product__seller=request.user
        ).distinct().order_by('-created_at')

    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'order-management.html', {'orders': orders, 'status_filter': status_filter})


@login_required
def update_order_status(request, order_id):
    if request.user.role not in ['admin', 'seller']:
        return redirect('home')

    from Seller.models import Order
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status in valid:
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} updated to {new_status}.')

    return redirect('order_management')


@login_required
def product_management_view(request):
    if request.user.role not in ['admin', 'seller']:
        messages.error(request, 'Access denied.')
        return redirect('home')

    from products.models import Product, Category
    from Seller.forms import ProductForm

    if request.user.role == 'admin':
        products = Product.objects.all().order_by('-created_at')
    else:
        products = Product.objects.filter(seller=request.user).order_by('-created_at')

    categories = Category.objects.all()

    search = request.GET.get('search', '')
    if search:
        products = products.filter(name__icontains=search)

    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category__id=category_id)

    if request.method == 'POST' and 'add_product' in request.POST:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" added!')
            return redirect('product_management')
        else:
            messages.error(request, 'Please fix the errors in the form.')
    else:
        form = ProductForm()

    return render(request, 'product-management.html', {
        'products': products, 'categories': categories,
        'form': form, 'search': search, 'category_id': category_id,
    })
