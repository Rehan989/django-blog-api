from django.shortcuts import render

# Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response

# Imports from Serializer
from .serializers import PostSerializer

# Models impor
from .models import Post

# Method for fetching LatsetBlogPosts
class LatestBlogPosts(APIView):
	def get(self, request, format=None):
		try:
			# Extracting Page Size from get body
			pageSize = request.data['pageSize']
			if(pageSize):
				blogPosts = Post.objects.all().exclude(publish_state="draft")[0:int(pageSize)]
				serializer = PostSerializer(blogPosts, many=True)
				# Returning Parsed Posts
				return Response(serializer.data)
			else:
				blogPosts = Post.objects.all().exclude(publish_state=="draft")[0:6]
				serializer = PostSerializer(blogPosts, many=True)
				# Return 6 latest Parsed posts if pageSize is not provided
				return Response(serializer.data)
		except Exception as e:
			print(e)
			return Response("Internal Server Error")


# Method for fetching Blogposts Through page Number
class BlogPosts(APIView):
	def get(self, request, format=None):
		try:
			# Defining pageSize of all the pages
			pageSize = 8
			pageNumber = request.data["pageNumber"]
			if(pageNumber):
				try:
					pageNumber = int(pageNumber)
					# Returning the bloposts according to blog page and pageSize
					blogPosts = Post.objects.all().exclude(publish_state="draft")[pageNumber*8:pageNumber*8+8]
					serializer = PostSerializer(blogPosts, many=True)
					# Sending data after parsing it
					return Response(serializer.data)
				except Exception as e:
					# print(e)
					# Returning empty list if blog pages value is 0
					return Response([])
			else:
				# Throwing Error if pageNumber is not provided
				return Response("No blog Posts to diplay!")
		except Exception as e:
			return Response("Internal Server Error")