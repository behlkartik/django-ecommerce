from enum import Enum
from django.db import models
from django.urls import reverse
from restaurant_app.models import BaseModel
from item.models import Item
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from .signals import (
    item_added_to_cart,
    item_removed_from_cart
)
from django.shortcuts import get_object_or_404

User = get_user_model()

# Create your models here.

class CartQuerySet(models.QuerySet):
    def search(self, query):
        if not query or query == "":
            return self.none() # []
        return self.filter(Q(cartitem__item__name__icontains=query) | Q(status__icontains=query))
    
    def by_customer(self, customer):
        return self.filter(customer=customer)

class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(model=self.model, using=self._db)
    def search(self, query):
        return self.get_queryset().search(query=query)
    
    def by_customer(self, customer):
        return self.get_queryset().by_customer(customer=customer)
    

class Cart(BaseModel):
    class CartStatus(Enum):
        NEW = "new"
        CHECKOUT = "checkout"
        PAID = "paid"
        ABANDONED = "abandoned"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]
        
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=CartStatus.choices(), default=CartStatus.NEW, max_length=30) 
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    
    
    def __str__(self) -> str:
        return f'Cart: {self.id} with status {self.status}'
    
    objects = CartManager()
    
class CartItem(BaseModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    prev_quantity = models.IntegerField(default=0)
    discount = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"CartItem: {self.quantity} of {self.item.name}"
        
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    
    # def delete(self, *args, **kwargs):
    #     super().delete(*args, **kwargs)

def cart_item_post_save(sender, instance, created, *args, **kwargs):
    if instance.prev_quantity > instance.quantity:
        print("quantity decreased!!!")
        item_removed_from_cart.send(sender=sender, instance=instance)
        
    elif instance.prev_quantity < instance.quantity:
        print("quantity increased!!!")
        item_added_to_cart.send(sender=sender, instance=instance)
    instance.prev_quantity = instance.quantity

def cart_item_post_delete(sender, instance, *args, **kwargs):
    print("item deleted!!!")
    item_removed_from_cart.send(sender=sender, instance=instance)

def get_total(cart):
    # cart = Cart.objects.by_customer(user).first()
    total = sum([ cart_item.quantity * cart_item.item.price for cart_item in cart.cartitem_set.all() ])
    return total

def update_cart_total(sender, instance, *args, **kwargs):
    cart = get_object_or_404(Cart, id=instance.cart.id)
    total = get_total(cart)
    cart.total = total
    cart.save()
        

post_save.connect(cart_item_post_save, CartItem)
post_delete.connect(cart_item_post_delete, CartItem)

item_added_to_cart.connect(update_cart_total)
item_removed_from_cart.connect(update_cart_total)
