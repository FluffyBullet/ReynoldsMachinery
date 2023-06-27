from .models import Company
from django import forms

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields =('company_name', 
                 'company_image',
                 'employees',
                 'phone_number',
                 'field_a',
                 'field_b',
                 'field_c',)
        