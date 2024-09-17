from unittest import TestCase
from django.contrib.auth import get_user_model
from .models import Order, OrderItem
from item.models import Item

User = get_user_model()

class UserTest(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='test', password='test@1234')
    
    def test_user_and_pwd(self) -> None:
        self.assertIsNotNone(self.test_user)
        checked = self.test_user.check_password("test@1234")
        self.assertTrue(checked)
    
    def tearDown(self) -> None:
        self.test_user.delete()

class OrderTest(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(username='test', password='test@1234')
        self.test_order = Order.objects.create(customer=self.test_user)
        self.test_item = Item.objects.create(name="test item", description="test item description", price=10.10, type="BV", veg_nonveg="Veg")
        self.order_item = OrderItem.objects.create(order=self.test_order, item=self.test_item, quantity=1)
        
    
    def test_customer_orders_reverse_relation(self):
        self.assertEqual(self.test_user.orders.count(), 1)
    
    def test_customer_orders(self):
        qs = Order.objects.filter(customer=self.test_user)
        self.assertTrue(qs.count(), 1)
    
    def test_order_item(self):
        qs = OrderItem.objects.filter(order=self.test_order).all()
        self.assertEqual(qs.count(), 1)
    
    def test_customer_order_item(self):
        qs = OrderItem.objects.filter(order__customer=self.test_user).all()
        self.assertEqual(qs.count(), 1)
    
    def test_customer_order_item_reverse(self):
        order_ids = list(self.test_user.orders.all().values_list('id', flat=True))
        qs = OrderItem.objects.filter(order__id__in=order_ids)
        self.assertEqual(qs.count(), 1)
        
    def tearDown(self) -> None:
        self.order_item.delete()
        self.test_item.delete()
        self.test_order.delete()
        self.test_user.delete()
