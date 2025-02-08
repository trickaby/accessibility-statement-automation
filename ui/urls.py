from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download/<path:file_path>', views.download_result, name='download_result'),
]