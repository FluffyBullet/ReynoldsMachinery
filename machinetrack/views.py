from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from .models import Company, Profile, MachineModel, MachineProfile, Job
from .forms import CompanyForm, JoinCompany, CreateModelForm, CreateAssetForm
from django.contrib import messages

# Create your views here.

# Display for home page
def Home(request):
    template = 'index.html'
    return render(request, template)

# Section for associated account
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
            profile = Profile.objects.get(username =request.user)

            try:
                company = Company.objects.get(company_name=company_name)
                if company.pin == pin:
                    messages.success(request, f"You have joined '{company_name}'.")
                    profile.company = company
                    profile.save()
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
        profile.company = None
        profile.save()
        messages.success(request, message)
        return redirect('home')

# Section for assets/machines
def create_model(request):
    if request.method == 'POST':
        form = CreateModelForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            message = f"{form_data['model_name']} has been created"
            model = MachineModel(
                manufacturer=form_data['manufacturer'],
                model_name=form_data['model_name'],
                fusion_type=form_data['fusion_type'],
                voltage=form_data['voltage'],
                image=form_data['image'],
                manufacturer_product_code=form_data['manufacturer_product_code']
            )
            model.save()
            messages.success(request, message)
            return redirect('home')
        else:
            message = f"{form.data['model_name']} is already an existing model"
            messages.error(request, message)
    else:
        form = CreateModelForm()

    return render(request, 'new_model.html', {'CreateModelForm': form})

def new_asset(request):
    if request.method == 'POST':
        form = CreateAssetForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            model_name = form_data['model']
            machine_model = MachineModel.objects.get(model=model_name)
            machine = MachineProfile(
                manufacturer_reference=form_data['manufacturer_reference'],
                company_reference=form_data['company_reference'],
                model=machine_model,
                serial_number=form_data['serial_number'],
                year_of_man=form_data['year_of_man'],
                status=form_data['status'],
                owner=form_data['owner'],
                is_electrical=form_data['is_electrical'],
                last_pat_test=form_data['last_pat_test'],
                last_calibration=form_data['last_calibration'],
            )
            message = f"`{model_name}` with s/n {form_data['serial_number']} has been added."
            machine.save()
            messages.success(request, message)
            return redirect('home')
        else:
            form_data = form.cleaned_data
            message = f"This machine is already added"
            messages.error(request, message)
    else:
        form = CreateAssetForm()

    return render(request, 'new_asset.html', {'CreateAssetForm': form})

# List through jobs relating to the company in query
@login_required
def job_list(request): 
    """
    Display view for all jobs with specific company
    """
    account =  request.user.profile
    jobs = Job.objects.filter(company_name_id=account.company)

    context = {
        'account': account,
        'jobs': jobs
    }

    return render(request, 'tracking_page.html', context)
