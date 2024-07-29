from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    session_id = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

class UserActivity(models.Model):
    session_id = models.CharField(max_length=40)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=50)  # e.g., 'viewed', 'added_to_cart', 'purchased'
    timestamp = models.DateTimeField(default=timezone.now)
    page = models.CharField(max_length=100, null=True, blank=True)
