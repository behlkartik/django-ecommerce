import django
import django.dispatch 
# Define custom signals
item_added_to_cart = django.dispatch.Signal(providing_args=['instance'])
item_removed_from_cart = django.dispatch.Signal(providing_args=['instance'])