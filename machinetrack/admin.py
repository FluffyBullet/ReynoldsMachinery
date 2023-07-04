from django.contrib import admin
from .models import Profile, Company, MachineModel, Job, MachineProfile

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

class MachineProfileAdmin(admin.ModelAdmin):
    list_display = (
        'manufacturer_reference',
        'company_reference',
        'model',
        'year_of_man',
        'status',
        'owner',
        'last_pat_test',
        'last_calibration',
    )
    filter_by = (
        'model',
        'year_of_man',
        'status',
        'owner',
        'last_pat_test',
        'last_calibration',
        )

class JobsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'machine_id',
        'created_by',
        'company_name',
    )
    filter_by = (
        'company_name',
        'created_by',
    )
    

admin.site.register(Profile, ProfileView)
admin.site.register(Company, CompanyView)
admin.site.register(MachineModel, MachineModelAdmin)
admin.site.register(Job,JobsAdmin)
admin.site.register(MachineProfile, MachineProfileAdmin)