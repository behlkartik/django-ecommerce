"""restaurant_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import index as home
from item.views import edit_item, list_items, show_item, create_item
from accounts.views import login_view, logout_view, register_view, change_password_view
from django.conf.urls.static import static
from django.conf import settings

from order.views import list_orders, update_order, show_order, cancel_order, cancel_orderitem, update_orderitem, create_order
from cart.views import add_to_cart, show_cart, update_cart

urlpatterns = [
    path('', home, name='home'),
    path('items/', list_items, name='list_items'),
    path('items/create', create_item, name='create_item'),
    path('items/<slug:slug>', show_item, name='show_item'),
    path('items/<slug:slug>/edit', edit_item, name='edit_item'),
    path('orders/', list_orders, name='list_orders'),
    path('orders/<int:order_id>', show_order, name='show_order'),
    path('orders/<int:order_id>/edit', update_order, name='update_order'),
    path('orders/<int:order_id>/cancel', cancel_order, name='cancel_order'),
    path('orders/<int:order_id>/orderitem/<int:orderitem_id>/edit', update_orderitem, name='edit_order_item'),
    path('orders/<int:order_id>/orderitem/<int:orderitem_id>/cancel', cancel_orderitem, name='cancel_order_item'),
    path('cart/', show_cart, name="show_cart"),
    path('orders/create', create_order, name='create_order'),
    path('cart/items/<int:item_id>', add_to_cart, name="add_to_cart"),
    path('cart/items/<int:item_id>/update', update_cart, name="update_cart"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('changepass/', change_password_view, name="changepass"),
    path('admin/', admin.site.urls, name='admin')
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)