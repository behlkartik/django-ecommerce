import os


from django.test import TestCase
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RestaurantApp(TestCase):
    def test_secret_key(self):
        self.assertIsNotNone(os.getenv("DJANGO_SECRET_KEY"))
        try:
            validate_password(os.getenv("DJANGO_SECRET_KEY"))
        except ValidationError as e:
            self.fail(f'Weak secret key {e}')
    
    def test_debug_set(self):
        self.assertIsNotNone(os.getenv("DEBUG"))