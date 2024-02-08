
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('set_organization/', views.set_organization),
#     path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
