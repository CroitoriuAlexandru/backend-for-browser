
from django.urls import path
from . import views

urlpatterns = [
    path('test_stuff/', views.test_stuff),
    
    path('set_organization/', views.set_organization.as_view()),
    path('generate_departments/', views.generate_company_departments.as_view()),
    path('set_caen_code/', views.set_caen_code.as_view()),
    path('set_nr_employees/', views.set_nr_employees.as_view()),
    path("set_company_departments/", views.set_company_departments.as_view()),
    path('get_user_employees_from_google/', views.get_user_employees_from_google.as_view()),
    
    path('get_organigram_info/', views.get_organigram_info.as_view()),
    path('set_employee_department_and_supervizer/', views.set_employee_department_and_supervizer.as_view()),
]