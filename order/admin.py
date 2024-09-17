from django.contrib import admin
from .models import Order, OrderItem
from restaurant_app.admin import BaseAdmin
from django import forms
# Register your models here.

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    fields = ["item", "order", "quantity"]
    readonly_fields = ["order"]
    

class OrderAdmin(BaseAdmin):
    model = Order
    inlines = [OrderItemInline]
    list_display = ["id", "customer", "status", "created_at", "updated_at"]
    readonly_fields = ["id"]
    raw_id_fields = ["customer"]
    search_fields = ["customer__username"]
    

class OrderItemAdmin(BaseAdmin):
    model = OrderItem
    list_display = ["id", "order", "item", "quantity", "created_at", "updated_at"]
    readonly_fields = ["id"]
    raw_id_fields = ["order", "item"]
    search_fields = ["order__customer__username", "item__name"]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)