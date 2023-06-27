from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Company
from .forms import CompanyForm

# Create your views here.

def Home(request):
    template = 'index.html'
    return render(request, template)

def CompanyOverview(request):
    queryset = Company.objects.all()
    template = 'create_company.html'
    context = {
        'CompanyForm': CompanyForm()
    }
    return render(request, template, context)
