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
from item.views import list_items, show_item, create_item
from accounts.views import login_view, logout_view, register_view, change_password_view

urlpatterns = [
    path('', home, name='home'),
    path('items/', list_items, name='list_items'),
    path('items/create', create_item, name='create_item'),
    path('items/<str:name>', show_item, name='show_item'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('changepass/', change_password_view, name="changepass"),
    path('admin/', admin.site.urls, name='admin'),
]
