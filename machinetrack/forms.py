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
        kwargs['min_value'] = 1900
        kwargs['max_value'] = datetime.date.today().year
        super().__init__(*args, **kwargs)
class YearSelectDateWidget(SelectDateWidget):
    def create_select(self, name, field, value, year_attrs, month_attrs, day_attrs):
        # Only display the year select element
        select_html = super().create_select(name, field, value, year_attrs, month_attrs, day_attrs)
        return select_html.replace('<select', '<select style="display: none;"')


class CreateAssetForm(forms.ModelForm):
    manufacture_reference = forms.CharField(max_length=25)
    company_reference = forms.CharField(max_length=25)
    model = forms.ChoiceField()

    serial_number = forms.CharField(max_length=30)
    year_of_man = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, datetime.date.today().year + 1)))
    status = forms.CharField(max_length=30)
    owner = forms.CharField(max_length=30)
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
        self.fields['model'].choices = [(model.id, model.model_name) for model in MachineModel.objects.all()]
