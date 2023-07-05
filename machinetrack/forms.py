from .models import Company, MachineModel, MachineProfile
from django import forms
from django.contrib import messages
import datetime
from django.forms.widgets import SelectDateWidget

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
        
# Custom widget to allow new_asset year of manufacturer to enter as year only.
class YearField(forms.IntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['min_value'] = 1980
        kwargs['max_value'] = datetime.date.today().year
        super().__init__(*args, **kwargs)

class YearSelectWidget(forms.Select):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.choices = self.get_year_choices()

    def get_year_choices(self):
        current_year = datetime.date.today().year
        return [(year, str(year)) for year in range(1980, current_year + 1)]

class CreateAssetForm(forms.ModelForm):
    manufacture_reference = forms.CharField(max_length=25)
    company_reference = forms.CharField(max_length=25)
    model = forms.ChoiceField()
    serial_number = forms.CharField(max_length=30)
    year_of_man = YearField(widget=YearSelectWidget())
    status = forms.CharField(max_length=30)
    owner = forms.ModelChoiceField(queryset=Company.objects.all())
    is_electrical = forms.BooleanField(initial=True, required=False)
    last_pat_test = forms.DateTimeField()
    last_calibration = forms.DateTimeField()

    class Meta:
        model = MachineProfile
        fields = ['manufacture_reference', 'company_reference', 'model',
                  'serial_number', 'year_of_man', 'status', 'owner',
                  'is_electrical', 'last_pat_test', 'last_calibration']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].choices = [(model.model_name, model.model_name) for model in MachineModel.objects.all()]