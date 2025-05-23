# inventory/models.py
from django.db import models, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Validate stock quantity before saving
        with transaction.atomic():
            if self.transaction_type == 'OUT':
                if self.product.stock_quantity < self.quantity:
                    raise ValidationError(
                        f"Cannot perform OUT transaction: insufficient stock for {self.product.name}. "
                        f"Available: {self.product.stock_quantity}, Requested: {self.quantity}"
                    )
            # Update stock quantity based on transaction type
            if self.transaction_type == 'IN':
                self.product.stock_quantity += self.quantity
            elif self.transaction_type == 'OUT':
                self.product.stock_quantity -= self.quantity
            self.product.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.transaction_type} - {self.quantity}"