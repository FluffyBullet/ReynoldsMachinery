from django.contrib import admin
from .models import Profile, Company, MachineModel

# Register your models here.

class ProfileView(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'company',
        
    )
    list_filter= (
        'company',
    )

class CompanyView(admin.ModelAdmin):
    list_display = (
        'company_name',
        'owner',
        'employees',
    )
    list_filter = (
        'owner',
    )

class MachineModelAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer',
        'model_name',
        'fusion_type',
        'manufacturer_product_code',
    )
    list_filter = (
        'manufacturer',
        'model_name',
        'fusion_type',
        'manufacturer_product_code',
    )
    

admin.site.register(Profile, ProfileView)
admin.site.register(Company, CompanyView)
admin.site.register(MachineModel, MachineModelAdmin)