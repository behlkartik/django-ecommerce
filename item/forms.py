from typing import Any
from django import forms
from django.forms import ValidationError
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        
    def clean_name(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get("name")
        qs = Item.objects.all().filter(name__icontains = name)
        if qs.exists():
            self.add_error('name', f"Item '{name}' already exists",)
        return name
    
    def clean_price(self):
        cleaned_data = self.cleaned_data
        price = cleaned_data.get("price")
        if price < 1.0:
            self.add_error('name', f"Price can't be less than 1",)
        return price
