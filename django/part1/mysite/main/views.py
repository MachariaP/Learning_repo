from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(response):
    return HttpResponse("<h1>Login!</h1>")

def dashboard(response):
    return HttpResponse("<h1>Dashboard!</h1>")

def login(response):
    return HttpResponse("<h1>Login!</h1>"))

