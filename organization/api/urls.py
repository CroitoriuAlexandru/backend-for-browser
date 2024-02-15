
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.get_routes),
    path('set_organization/', views.set_organization),
    path('generate_departments/', views.generate_departments),
    path('get_mails/', views.get_mails),
]
