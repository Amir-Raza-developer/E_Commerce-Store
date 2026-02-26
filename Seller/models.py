from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('card',   'Credit / Debit Card'),
        ('paypal', 'PayPal'),
        ('cod',    'Cash on Delivery'),
    ]

    buyer          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    total          = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Shipping info saved at time of order
    full_name      = models.CharField(max_length=100)
    email          = models.EmailField()
    phone          = models.CharField(max_length=15, blank=True)
    address        = models.TextField()
    city           = models.CharField(max_length=100)
    state          = models.CharField(max_length=100, blank=True)
    zip_code       = models.CharField(max_length=20, blank=True)

    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2)  # price locked at purchase time

    def get_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
