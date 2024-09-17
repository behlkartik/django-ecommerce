from django.test import TestCase
from .models import Item
from django.utils.text import slugify
from django.forms import ValidationError
from .forms import ItemForm

# Create your tests here.
class ItemTest(TestCase):
    def setUp(self):
        self.number_of_items = 10
        for _ in range(self.number_of_items):
            Item.objects.create(name="Coke", price=30.40, description="Coca cola drink")
        
    def test_queryset_exist(self):
        self.assertTrue(Item.objects.all().exists())
    
    def test_queryset_count(self):
        self.assertTrue(Item.objects.all().count() == self.number_of_items)
        
    def test_name_slugified(self):
        item = Item.objects.all().order_by("id").first()
        self.assertEqual(item.slug, slugify(item.name))
    
    def test_name_slugified_unique(self):
        qs = Item.objects.all().exclude(slug="coke")
        for item in qs:
            self.assertNotEqual(item.slug, slugify(item.name))
    
    def test_create_unique_slug(self):
        existing_slug_list = Item.objects.all().values_list('slug', flat=True)
        self.assertEqual(len(existing_slug_list), len(list(set(existing_slug_list))))
        # new_slugs = []
        # for item in qs:
        #     new_slugs.append(create_unique_slug(item, item.slug))
        
        # new_slugs = list(set(new_slugs))
        # self.assertEqual(len(new_slugs), qs.count())
    
    def test_user_added_slug_not_unique(self):
        form = ItemForm(data=dict(name="Coke", price=30.40, description="coca cola drink", slug="coke", type="BV", veg_nonveg="Veg"))
        self.assertFalse(form.is_valid())
        self.assertIn('slug', form.errors.keys())
        
    def test_search_item_manager(self):
        qs = Item.objects.search(query="coke")
        self.assertEqual(qs.count(), self.number_of_items)
        
        qs = Item.objects.search(query="cola")
        self.assertEqual(qs.count(), self.number_of_items)
        
        qs = Item.objects.search(query="non existing")
        self.assertEqual(qs.count(), 0)
        
    
        