from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'external_id',
            'code',
            'description',
            'name',
            'barcode',
            'retail_price',
            'wholesale_price',
            'discount'
        ]