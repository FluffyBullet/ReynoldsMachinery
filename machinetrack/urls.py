from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('create-company/', views.create_company, name="create_company"),
    path('edit-company/<str:company>/', views.edit_company, name="edit_company"),
    path('join-company/', views.join_company, name="join_company"),
    path('leave-company/', views.leave_company, name="leave_company"),
    path('create-model/', views.create_model, name="create_model"),
    path('create-asset/', views.new_asset, name="new_asset"),
    path('tracking/', views.job_list, name='tracker'),
    path('jobs/<int:job_id>/', views.JobDetailsView.as_view(), name='job_detail'),
    path('jobs/edit/<int:job_id>/', views.EditJobView.as_view(), name='job_edit'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    ] 