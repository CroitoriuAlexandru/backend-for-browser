from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("register-organization", views.registerOrganization, name="registerOrganization"),
    path("organigramPage", views.organigramPage, name="organigramPage"),
    path("create-employee", views.create_employee, name="create_employee"),
    path("delete-employee/<int:pk>", views.delete_employee, name="delete_employee"),
    path("create-department", views.create_department, name="create_department"),
    path("delete-department/<int:pk>", views.delete_department, name="delete_department"),
]
