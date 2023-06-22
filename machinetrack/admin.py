from django.contrib import admin
from .models import Profile

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

admin.site.register(Profile, ProfileView)