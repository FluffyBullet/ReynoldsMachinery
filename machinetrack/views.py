from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Company, Profile
from .forms import CompanyForm, JoinCompany
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
                profile.company = company.company_name
                profile.save()
                message = f"Your company `{company.company_name}` has been created"
                messages.success(request, message)
                return redirect('home')
            else: 
                print(form.errors)
                messages.warning(request, 'Your company is already existing')
    else:
        form = CompanyForm()
    return render(request, 'create_company.html', {'CompanyForm':CompanyForm})        

def edit_company(request, company):
    company = get_object_or_404(Company, company_name=company)

    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details updated")
            return redirect('home')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'edit_company.html', {'CompanyForm': form})

def join_company(request):
    if request.method == 'POST':
        form = JoinCompany(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            pin = form.cleaned_data['pin']

            try:
                company = Company.objects.get(company_name=company_name)
                if company.pin == pin:
                    profile = Profile.objects.get(username =request.user)
                    profile.company = company_name
                    profile.save()
                    messages.success(request, f"You have joined '{company_name}'.")
                    return redirect('home')
                else:
                    messages.error(request, 'Pin entry is incorrect')
            except Company.DoesNotExist:
                messages.error(request, 'Company does not exist')
        else:
            messages.error(request, 'Form data is invalid')
    else:
        form = JoinCompany()

    return render(request, 'join_company.html', {'JoinCompany': JoinCompany})

def leave_company(request):
     profile = request.user.profile

     if profile.company == "":
        messages.error(request, ' you are not part of a company.')
        return redirect('home')       
     else :
        message = f'You have left {profile.company}'
        profile.company = ""
        profile.save()
        messages.success(request, message)
        return redirect('home')

            