from django.contrib import admin
from django.urls import path, include
from djoser.conf import User 

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls.authtoken')),
]
