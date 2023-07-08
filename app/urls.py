from django.urls import path
from . import views
from django.contrib.staticfiles.views import serve


urlpatterns = [
    path('', views.handle),
    path('process/', views.process_hash),
    path('favicon.ico', serve, {'path': 'img/favicon.ico'}),
]

