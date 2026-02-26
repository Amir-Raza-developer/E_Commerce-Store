from django import forms
from products.models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'category', 'description', 'price', 'stock', 'image', 'is_active']
        widgets = {
            'name':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'category':    forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Product description...'}),
            'price':       forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'stock':       forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'image':       forms.FileInput(attrs={'class': 'form-control'}),
            'is_active':   forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
