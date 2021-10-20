from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls.authtoken')),
    path('activate-account/<str:uid>/<str:token>/', views.UserActivationView.as_view(), name='activate-email')
]
