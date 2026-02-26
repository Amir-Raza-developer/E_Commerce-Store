from django.urls import path
from . import views

urlpatterns = [
    # Product Management
    path('product-management/',           views.product_management,  name='product_management'),
    path('product-management/edit/<int:pk>/',   views.edit_product,  name='edit_product'),
    path('product-management/delete/<int:pk>/', views.delete_product, name='delete_product'),

    # Order Management
    path('order-management/',             views.order_management,    name='order_management'),
    path('order-management/<int:pk>/',    views.order_detail,        name='order_detail'),
    path('order-management/update/<int:pk>/', views.update_order_status, name='update_order_status'),
]
