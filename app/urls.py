from django.urls import path
from . import views

urlpatterns = [
    path('', views.handle),
    path('process/', views.process_number, name='process_number'),
]