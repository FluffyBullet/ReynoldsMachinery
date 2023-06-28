from .models import Company
from django import forms
from django.contrib import messages

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields =('company_name', 
                 'company_image',
                 'employees',
                 'phone_number',
                 'field_a',
                 'field_b',
                 'field_c',
                 'pin',)
        
    def clean_name(self):
        company_name = self.cleaned_data.get('company_name')
        if Company.objects.filter(company_name = company_name).exists():
            raise forms.ValidationError("This company is already raised")
        return company_name
        