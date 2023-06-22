from django.contrib import admin
from .models import Profile, Company

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

admin.site.register(Profile, ProfileView)
admin.site.register(Company, CompanyView)