from django.contrib import admin
from django.urls import path, include 

from .views import LatestBlogPosts, BlogPosts, SingleBlogPosts, Addlike, RemoveLike, AddComment
# Url Patterns for blog api endpoint
urlpatterns = [
    path('latest-posts/', LatestBlogPosts.as_view()),
    path('getposts/', BlogPosts.as_view()),
    path('post/', SingleBlogPosts.as_view()),
    path('post/addlike/', Addlike.as_view()),
    path('post/removelike/', RemoveLike.as_view()),
    path('post/addcomment/', AddComment.as_view()),
]