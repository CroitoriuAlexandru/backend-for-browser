
from django.urls import path
from . import views

urlpatterns = [
    path('add_background_image/', views.add_background_image.as_view(), name='add-background-image'),
    path('get_background_images/', views.get_background_images.as_view(), name='get-background-images'),
    path('remove_background_image/', views.remove_background_image.as_view(), name='remove-background-image'),
    path('save_most_used_sites/', views.save_most_used_sites.as_view(), name='save-most-used-sites'),
]