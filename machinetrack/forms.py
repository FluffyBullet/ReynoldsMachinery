from .models import Company, MachineModel   
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
    
class JoinCompany(forms.Form):
    company_name = forms.CharField(label="Company Name")
    pin = forms.IntegerField(label="pin")
        

class CreateModelForm(forms.ModelForm):
    class Meta:
        model = MachineModel
        fields = ['manufacturer', 'model_name',
                   'fusion_type', 'image', 
                   'voltage', 'manufacturer_product_code']
