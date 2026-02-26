from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.home_view,           name='home'),
    path('shop/',                         views.shop_view,           name='shop'),
    path('product/<int:pk>/',             views.product_detail_view, name='product_detail'),
    path('cart/',                         views.cart_view,           name='cart'),
    path('cart/add/<int:pk>/',            views.add_to_cart,         name='add_to_cart'),
    path('cart/remove/<int:pk>/',         views.remove_from_cart,    name='remove_from_cart'),
    path('cart/update/<int:pk>/',         views.update_cart,         name='update_cart'),
    path('checkout/',                     views.checkout_view,       name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view,  name='order_success'),
    path('wishlist/<int:pk>/',            views.toggle_wishlist,     name='toggle_wishlist'),
]