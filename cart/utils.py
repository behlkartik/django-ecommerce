
from django.shortcuts import get_object_or_404
from .models import Cart

def get_total(cart):
    # cart = Cart.objects.by_customer(user).first()
    total = sum([ cart_item.quantity * cart_item.item.price for cart_item in cart.cartitem_set.all() ])
    return total

def update_cart_total(sender, instance, *args, **kwargs):
    cart = get_object_or_404(Cart, customer=instance.user)
    total = get_total(cart)
    cart.total = total
    cart.save()
    