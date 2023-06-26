from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Company

# Create your views here.

def home(request):
    template = 'index.html'
    return render(request, template)

def company_overview(request):
    queryset = Company.objects.all()
