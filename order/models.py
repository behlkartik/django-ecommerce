from django.db import models
from django.conf import settings
from item.models import Item
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from enum import Enum
from django.db.models import Q

from restaurant_app.models import BaseModel

# Create your models here.

User = settings.AUTH_USER_MODEL

class OrderStatus(Enum):
    PENDING = "pending"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
    
class AddressType(Enum):
    BILLING = "billing"
    SHIPPING = "shipping"
    
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class OrderQuerySet(models.QuerySet):
    def search(self, query):
        if not query or query == "":
            return self.none() # []
        return self.filter(Q(orderitem__item__name__icontains=query) | Q(orderitem__item__description__icontains=query))
         

class OrderManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return OrderQuerySet(model=Order, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query)
    
class Order(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=OrderStatus.choices(), max_length=20, default=OrderStatus.PENDING.value)
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=20)
    
    
    @staticmethod
    def get_by_id(order_id):
        orders = list(filter(lambda order: order.id == order_id, Order.objects.all()))
        return None if not orders else orders[0]
    
    def get_absolute_url(self):
        return reverse("show_order", kwargs={"order_id": self.id})
    
    def get_update_url(self):
        return reverse("update_order", kwargs={"order_id": self.id})
    
    def update_total(self):
        _total = sum([ order_item.quantity * order_item.item.price for order_item in self.orderitem_set.all() ])
        self.total = _total
        self.save()
    
    def __str__(self) -> str:
        return str(self.id)
    
    objects = OrderManager()

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def get_edit_url(self):
        return reverse("edit_order_item", kwargs={"order_id": self.order.id, "order_item_id": self.id})
    
    def get_cancel_url(self):
        return reverse("cancel_order_item", kwargs={"order_id": self.order.id, "order_item_id": self.id})
    
    def __str__(self) -> str:
        return "Item: {self.item.name}, Order: {self.order.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_total()
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_total()


class UserAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    address_type = models.CharField(choices=AddressType.choices(), max_length=20)
    
    def __str__(self) -> str:
        return f"{self.street}, {self.city}, {self.country} ({self.get_address_type_display()})"