from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrator'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]
    role    = models.CharField(max_length=20, choices=ROLES, default='buyer')
    phone   = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='administrator_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='administrator_users',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"