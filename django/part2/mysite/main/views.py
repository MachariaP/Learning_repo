from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(response):
    return HttpResponse("<h1>Home Page!</h1>")

def about(response):
    return HttpResponse("<h1>About Page!</h1>")

def contact(response):
    return HttpResponse("<h1>Contact Page!</h1>")

def login(response):
    return HttpResponse("<h1>Login Page!</h1>")