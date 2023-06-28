from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('create-company/', views.create_company, name="create_company"),
    path('edit-company/<str:company>/', views.edit_company, name="edit_company"),
    ] 