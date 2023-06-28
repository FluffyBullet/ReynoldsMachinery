from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Company, Profile
from .forms import CompanyForm
from django.contrib import messages

# Create your views here.

def Home(request):
    template = 'index.html'
    return render(request, template)


def create_company(request):
    if request.method =='POST':
            form = CompanyForm(request.POST)
            if form.is_valid():
                company = form.save(commit=False)
                profile = Profile.objects.get(username = request.user.profile.username)
                company.owner = profile
                company.save()
                messages.success(request, 'Your company has been created')
                return redirect('home')
            else: 
                print(form.errors)
                messages.warning(request, 'Your company is already existing')
    else:
        form = CompanyForm()
    return render(request, 'create_company.html', {'CompanyForm':CompanyForm})        

# def CompanyOverview(request):
#     queryset = Company.objects.all()
#     template = 'create_company.html'
#     context = {
#         'CompanyForm': CompanyForm()
#     }

#     def post(self, request, *args, **kwargs):
#        if request.method =='POST':
#             form = CompanyForm(request.POST)
#             if form.is_valid():
#                 Company.instance.owner = request.user.username
#                 form.save
#                 return redirect('home')
#             else:
#                 form = CompanyForm()

#     return render(request, template, context)


