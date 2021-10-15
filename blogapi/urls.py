from django.contrib import admin
from django.urls import path, include 

from .views import LatestBlogPosts, BlogPosts
# Url Patterns for blog api endpoint
urlpatterns = [
    path('latest-posts/', LatestBlogPosts.as_view()),
    path('getposts/', BlogPosts.as_view()),
]