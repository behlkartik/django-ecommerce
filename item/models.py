from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.conf import settings
from restaurant_app.models import BaseModel


User = settings.AUTH_USER_MODEL
    

class ItemQuerySet(models.QuerySet):
    def search(self, query):
        if not query or query == "":
            return self.none() # []
        return self.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
    def get_by_item_type(self, type):
        return self.filter(type=type)
    
    def get_by_veg_nonveg(self, veg_nonveg):
        return self.filter(veg_nonveg=veg_nonveg)
    
class ItemManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return ItemQuerySet(model=self.model, using=self._db)
    
    def search(self, query):
        return self.get_queryset().search(query=query)
    
    def get_by_item_type(self, type):
        return self.get_queryset().all().get_by_item_type(type)
    
    def get_by_veg_nonveg(self, veg_nonveg):
        return self.get_queryset().all().get_by_veg_nonveg(veg_nonveg)
    
class Item(BaseModel):
    class Type(models.TextChoices):
        BEVERAGE = "BV", _("beverage")
        APPETIZER = "AP", _("appetizer")
        MAIN = "MA", _("main")
        SIDE = "SD", _("side")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(null=False, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=False, max_length=300)
    type = models.CharField(max_length=2, choices=Type.choices, default=Type.BEVERAGE.value)
    veg_nonveg = models.CharField(choices=[("v", "veg"), ("nv", "non-veg")], max_length=7, default="Veg")
    slug = models.SlugField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="items/")
    
    def get_absolute_url(self):
        return reverse("show_item", kwargs={"slug": self.slug})
    
    def get_create_url(self):
        return reverse("create_item")
    
    def __str__(self) -> str:
        return self.name
    
    objects = ItemManager()

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

