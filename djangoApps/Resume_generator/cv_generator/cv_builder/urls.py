from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_profile, name='create_profile'),
    path('success/', views.success, name='success'),
]