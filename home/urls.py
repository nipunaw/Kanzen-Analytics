from django.urls import path
from . import views
from home.dash_apps.finished_apps import init

urlpatterns = [
    path('', views.home, name='home'),
    path('edit/', views.edit, name='edit'),
    path('export/', views.export, name='export')
]