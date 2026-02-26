from django.urls import path
from . import views

urlpatterns = [
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/',   views.logout_view,   name='logout'),
    path('profile/',  views.profile_view,  name='profile'),

    path('order-management/',              views.order_management_view,  name='order_management'),
    path('order-management/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('product-management/',            views.product_management_view, name='product_management'),
]