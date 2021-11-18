from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls.authtoken')),
    path('auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('activate-account/<str:uid>/<str:token>/', views.UserActivationView.as_view(), name='activate-email'),
    path('reset-password/<str:uid>/<str:token>/', views.UserResetPassword.as_view(), name='reset-password'),
    path('reset-username/<str:uid>/<str:token>/', views.UserResetUsername.as_view(), name='reset-username'),
]
