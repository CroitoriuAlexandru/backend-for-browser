
from django.urls import path
from . import views
from .views import google_auth

urlpatterns = [
    path('', views.get_routes),
    path('google/', views.google_auth),
]
