from django.apps import AppConfig
from django.shortcuts import get_object_or_404


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
    
    # def ready(self) -> None:
    #     from django.db.models.signals import post_save
    #     Cart = self.get_model('Cart')
    #     post_save.connect(cart_post_save, Cart)

# def cart_post_save(sender, instance, created, *args, **kwargs):
#     klass = instance.__class__
#     cart = get_object_or_404(klass=klass, id=instance.id)
#     _total = sum([ cart_item.quantity * cart_item.item.price for cart_item in cart.cartitem_set.all() ])
#     instance.total = _total
#     if not created:
#         instance.save()