from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('machinetrack.urls'), name='tracking_site'),
    path('accounts/', include('allauth.urls')),
]
