from django.apps import AppConfig
from .utils import create_unique_slug


class ItemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'item'
    
    def ready(self) -> None:
        from django.db.models.signals import pre_save, post_save
        # from .models import Item
        Item = self.get_model('Item')
        pre_save.connect(item_pre_save, Item)
        post_save.connect(item_post_save, Item)

def item_pre_save(sender, instance, *args, **kwargs):
    instance.slug = create_unique_slug(instance, instance.slug)
    # instance.created_by = default_created_by(instance)

def item_post_save(sender, instance, created, *args, **kwargs):
    print("slugified name after save", instance.slug, created)
    
