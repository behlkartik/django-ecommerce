from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(null=False, max_length=200)
    price = models.FloatField(null=False)
    description = models.TextField(null=False, max_length=300)