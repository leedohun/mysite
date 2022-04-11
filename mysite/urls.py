"""mysite URL Configuration

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
from django.urls import path, include
import upsell.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upsell.views.home, name = 'home'),
    path('products/', upsell.views.products, name = 'products'),
    path('orders/', upsell.views.orders, name = 'orders'),
    path('categories/', upsell.views.categories, name = 'categories'),
    path('order_item/', upsell.views.order_item, name = 'order_item'),
    path('products_by_categories/', upsell.views.products_by_categories, name = 'products_by_categories'),
]
