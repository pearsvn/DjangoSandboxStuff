from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
        ]

# Not sure if this file is necessary anymore