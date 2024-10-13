from django.shortcuts import render, redirect
from .models import Profile

# Create your views here.
def create__profile(request):
    if request.method == 'POST':
        Profile = Profile(
            name=request.POST['name'],
            phone_number=request.POST['phone_number'],
            email=request.POST['email'],
            degree=request.POST['degree'],
            skills=request.POST['skills'],
            about=request.POST['about']
        )