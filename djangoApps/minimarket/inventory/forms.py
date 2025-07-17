from django import forms
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock_quantity', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Product Name',
            'category': 'Category',
            'price': 'Price ($)',
            'stock_quantity': 'Stock Quantity',
            'description': 'Description',
        }
        help_texts = {
            'name': 'Enter the name of the product.',
            'category': 'Select a category for the product.',
            'price': 'Enter the price in USD.',
            'stock_quantity': 'Enter the available stock quantity.',
            'description': 'Provide a brief description of the product.',
        }
        error_messages = {
            'name': {
                'required': 'This field is required.',
                'max_length': 'This field cannot exceed 200 characters.',
            },
            'price': {
                'required': 'This field is required.',
                'invalid': 'Enter a valid price.',
            },
            'stock_quantity': {
                'required': 'This field is required.',
                'invalid': 'Enter a valid stock quantity.',
            },
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'quantity', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'transaction_type': 'Transaction Type',
            'quantity': 'Quantity',
            'notes': 'Notes',
        }
        help_texts = {
            'transaction_type': 'Select the type of transaction.',
            'quantity': 'Enter the quantity for the transaction.',
            'notes': 'Provide any additional notes.',
        }
        error_messages = {
            'quantity': {
                'required': 'This field is required.',
                'invalid': 'Enter a valid quantity.',
            },
        }