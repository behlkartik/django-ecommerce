from django.contrib import admin
from order.models import Order, OrderItem
from django.contrib.auth import get_user_model

# Register your models here.
User = get_user_model()
admin.site.unregister(User)

class OrderInline(admin.StackedInline):
    model = Order
    extra = 0
    fields = ["customer", "status", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at", "status"]
    
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    inlines = [OrderInline]
    
admin.site.register(User, UserAdmin)