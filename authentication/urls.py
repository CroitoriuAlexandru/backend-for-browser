from django.urls import path
from . import views

urlpatterns = [
   path("auth/google/", views.GoogleLoginApi.as_view(), name="login-with-google"),
   path("googleUserList/", views.GoogleUserListApi.as_view(), name="google-user-list"),
]
