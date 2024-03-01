
from django.urls import path
from . import views

urlpatterns = [
    path('set_organization/', views.set_organization),
    path('generate_departments/', views.generate_company_departments.as_view()),
    path('set_caen_code/', views.set_caen_code.as_view()),
    path('set_nr_employees/', views.set_nr_employees.as_view()),
    path("set_company_departments/", views.set_company_departments.as_view()),

    
    path('get_organigram_info/', views.get_organigram_info.as_view()),
    path('set_employee_department/', views.set_employee_department.as_view()),
]
