from django.contrib import admin
from django.urls import path, include 

from .views import LatestBlogPosts, BlogPosts, FetchBlogPost, Addlike, RemoveLike, AddComment, SearchPost, FetchComments, AddContact
# Url Patterns for blog api endpoint
urlpatterns = [
    path('latest-posts/', LatestBlogPosts.as_view()),
    path('getposts/<int:pageNumber>', BlogPosts.as_view()),
    path('post/<str:slug>', FetchBlogPost.as_view()),
    path('post/<str:slug>/comments/', FetchComments.as_view()),
    path('post/addlike/', Addlike.as_view()),
    path('post/removelike/', RemoveLike.as_view()),
    path('post/addcomment/', AddComment.as_view()),
    path('search', SearchPost.as_view(), name="search"),
    path('contact/', AddContact.as_view(), name="contact")
]