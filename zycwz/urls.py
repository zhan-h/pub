import django.urls as urls
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
]
