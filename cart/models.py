from enum import Enum
from django.db import models
from django.urls import reverse
from restaurant_app.models import BaseModel
from item.models import Item
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your models here.

class CartQuerySet(models.QuerySet):
    def search(self, query):
        if not query or query == "":
            return self.none() # []
        return self.filter(Q(cartitem__item__name__icontains=query) | Q(status__icontains=query))

class CartManager(models.Manager):
    def get_queryset(self):
        return CartQuerySet(model=self.model, using=self._db)
    def search(self, query):
        return self.get_queryset().search(query=query)

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
    
    def update_total(self):
        _total = sum([ cart_item.quantity * cart_item.item.price for cart_item in self.cartitem_set.all() ])
        print("totall", _total)
        self.total = _total
        self.save()
    
    objects = CartManager()
    
class CartItem(BaseModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    discount = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"CartItem: {self.quantity} of {self.item.name}"
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_total()
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.cart.update_total()
        
