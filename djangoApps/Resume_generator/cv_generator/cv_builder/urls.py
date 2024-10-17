from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_profile, name='create_profile'),
    path('success/<int:profile_id>/', views.success, name='success'),
    path('generate_pdf/<int:profile_id>/', views.generate_pdf, name='generate_pdf'),
]