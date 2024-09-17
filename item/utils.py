from django.utils.text import slugify
from random import randrange
from django.db import models

def create_unique_slug(instance: models.Model, slug: str, is_new: bool = False):
    print("inside create unique slug", slug)
    if not slug:
        slug = slugify(instance.name)
    instance_class = instance.__class__
    qs = instance_class.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        if is_new:
            random_new_slug = f"{instance.slug}-{randrange(1, 10000)}"    
        else:
            random_new_slug = f"{slug}-{randrange(1, 10000)}"
        slug = create_unique_slug(instance, random_new_slug, True)
    return slug
