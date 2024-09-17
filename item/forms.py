from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        exclude = ['created_at', 'updated_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'placeholder': f'Item {field}'})
        self.fields["slug"].disabled = True
        
    # def clean_name(self):
    #     cleaned_data = self.cleaned_data
    #     name = cleaned_data.get("name")
    #     qs = Item.objects.all().filter(name__icontains = name)
    #     if qs.exists():
    #         self.add_error('name', f"Item '{name}' already exists",)
    #     return name
    
    def clean_price(self):
        cleaned_data = self.cleaned_data
        price = cleaned_data.get("price")
        if price < 1.0:
            self.add_error('name', f"Price can't be less than 1",)
        return price

    def clean_slug(self):
        cleaned_data = self.cleaned_data
        slug = cleaned_data.get("slug")
        qs = Item.objects.filter(slug__iexact=slug).all()
        if qs.exists():
            self.add_error("slug", f"Slug {slug} already exists for Item")
        return slug
