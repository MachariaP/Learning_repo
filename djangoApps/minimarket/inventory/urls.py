from django.urls import path
from django.contrib import admin
from inventory import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/transaction/add/', views.add_transaction, name='add_transaction'),
]