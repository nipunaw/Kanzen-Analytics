from django.urls import path
from . import views
from home.dash_apps.finished_apps import simpleexample
from home.dash_apps.finished_apps import creategraphs
urlpatterns = [
    path('', views.home, name='home')
]