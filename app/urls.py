from django.urls import path
from . import views
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path('', views.handle, name='index'),
    path('applicant/', views.handle_applicant, name='applicant'),
    path('employer/', views.handle_employer, name='employer'),

    path('submit/', views.process),

    path('favicon.ico', serve, {'path': 'img/favicon.ico'}),
]
