from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/success/', views.video_upload_success, name='video_upload_success'),
]