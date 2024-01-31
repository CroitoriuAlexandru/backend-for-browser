from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("register-organization", views.registerOrganization, name="registerOrganization"),
    path("organigram", views.get_organigram, name="organigram"),
]
