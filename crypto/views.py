from django.shortcuts import render
import requests


def index(request):
    
    context = {}
    return render(request, 'index.html')