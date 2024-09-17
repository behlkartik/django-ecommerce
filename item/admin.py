from django.contrib import admin
from .models import Item
from restaurant_app.admin import BaseAdmin

# Register your models here.
class ItemAdmin(BaseAdmin):
    list_display = ["id", "slug", "name", "price", "description", "type", "veg_nonveg", "created_at", "updated_at", "user"]
    search_fields = ["name", "description"]
    raw_id_fields = ["user"]

    
admin.site.register(Item, ItemAdmin)