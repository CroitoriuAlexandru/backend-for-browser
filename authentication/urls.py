from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
   path("auth/google/", views.GoogleLoginApi.as_view(), name="login-with-google"),
   path("googleUserList/", views.GoogleUserListApi.as_view(), name="google-user-list"),
   
   path("auth/regular-login/", views.RegularLoginApi.as_view(), name="regular-login"),
   path("uesr-profile/", views.UserProfileApi.as_view(), name="user-profile"),
   
   path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
