from django.urls import path
from authentication import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("auth/google/", views.GoogleLoginApi.as_view(), name="login-with-google"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("auth/regular-login/", views.RegularLoginApi.as_view(), name="regular-login"),

    path("uesr/profile/", views.UserProfileApi.as_view(), name="user-profile"),
    path("user/setfirstname/", views.SetFirstNameApi.as_view(), name="set-first-name"),
    path("user/setlastname/", views.SetLastNameApi.as_view(), name="set-last-name"),
    path("user/setusername/", views.SetUsernameApi.as_view(), name="set-username"),
    path("user/setphoto/", views.SetUserPhotoApi.as_view(), name="set-photo"),
    path("user/setphone/", views.SetUserPhoneApi.as_view(), name="set-user-phone"),
    path("user/setpassword/", views.setUserPasswordApi.as_view(), name="set-user-password"),
    
]
