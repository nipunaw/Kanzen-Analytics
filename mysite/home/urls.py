from django.urls import path
from . import views

#import any other dash apps here
from .dash_apps.finished_apps import simpleexample
urlpatterns = [
    path('',views.home, name='home')
]
