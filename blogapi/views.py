from django.shortcuts import render

# Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response

from userauthapi.serializers import User

# Imports from Serializer
from .serializers import PostSerializer,CommentSerializer

# Models impor
from .models import Post, BlogComment, Likes

# Method for fetching LatsetBlogPosts
class LatestBlogPosts(APIView):
	def get(self, request, format=None):
		try:
			# Extracting Page Size from get body
			pageSize = request.data['pageSize']
			blogPosts = Post.objects.all().exclude(publish_state="draft")[0:int(pageSize)]
			serializer = PostSerializer(blogPosts, many=True)
			# Returning Parsed Posts
			return Response({"posts":serializer.data, "success":"Success!"})
		except KeyError:
			blogPosts = Post.objects.all().exclude(publish_state="draft")[0:6]
			serializer = PostSerializer(blogPosts, many=True)
			# Return 6 latest Parsed posts if pageSize is not provided
			return Response({"posts":serializer.data, "success":"Success!"})
		except Exception as e:
			return Response({"error":"Internal Server Error"})


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
					return Response({"posts":serializer.data, "success":"Success!"})
				except KeyError:
					return Response({"posts":[], "success":"Success!"})
				except Exception as e:
					# print(e)
					# Returning empty list if blog pages value is 0
					return Response({"error":"Internal Servor Error!"})
			else:
				# Throwing Error if pageNumber is not provided
				return Response({"error":"Not found!"})
		except Exception as e:
			return Response({"error":"Internal Server Error"})


# Method for fetching the blog posts with comments
class SingleBlogPosts(APIView):
	def get(self, request, format=None):
		try:
			# Extracting Page Size from get body
			sno = request.data['sno']
			if(sno):
				post = Post.objects.get(sno=sno)
				comments = BlogComment.objects.filter(post=post)
				commentSerializer = CommentSerializer(comments, many=True)
				postSerializer = PostSerializer(post)
				# Returning Parsed Post
				return Response({"post": postSerializer.data, "comments":commentSerializer.data, "success":"Blog found Successfully"})
			else:
				return Response({"error":"Not found!"})
		except Exception as e:
			print(e)
			return Response({"error":"Internal Server Error"})


# Method for Adding likes to blog post
class Addlike(APIView):
	def put(self, request, format=None):
		try:
			# Extracting Page Size from get body
			email = request.data['email']
			username = request.data['username']
			postSno = request.data['sno']
			if(email, username):
				try:
					user = User.objects.get(email=email, username=username)
					if(user):
						post = Post.objects.get(sno=postSno)
						if(post):
							post.likes.add(user)
							post.save()
							return Response({"error":f"Updated Succesfully! Total likes: {post.total_likes()}"})
						else:
							return Response({"error":"Post not found!"})
					else:
						return Response({"error":"User not found!"})
				except Exception as e:
					print(e)
					return Response({"error":"Internal servor error!"})
		except KeyError:
			return Response({"error":"Fields not provided!"})
		except Exception as e:
			print(e)
			return Response({"error":"Internal Server Error"})


# Method for Removing likes from blog post
class RemoveLike(APIView):
	def post(self, request, format=None):
		try:
			# Extracting Page Size from get body
			email = request.data['email']
			username = request.data['username']
			postSno = request.data['sno']
			if(email, username):
				try:
					user = User.objects.get(email=email, username=username)
					if(user):
						post = Post.objects.get(sno=postSno)
						if(post):
							post.likes.remove(user)
							post.save()
							return Response({"error":f"Updated Succesfully! Total likes: {post.total_likes()}"})
						else:
							return Response({"error":"Post not found!"})
					else:
						return Response({"error":"User not found!"})
				except Exception as e:
					print(e)
					return Response({"error":"Internal servor error!"})
		except KeyError:
				return Response({"error":"Fields not provided!"})
		except Exception as e:
			print(e)
			return Response({"error":"Internal Server Error"})


# Method for Removing likes from blog post
class AddComment(APIView):
	def post(self, request, format=None):
		try:
			# Extracting Page Size from get body
			email = request.data['email']
			username = request.data['username']
			postSno = request.data['sno']
			commentBody = request.data['commentBody']
			if(email, username, postSno,commentBody):
				try:
					user = User.objects.get(email=email, username=username)
					if(user):
						post = Post.objects.get(sno=postSno)
						if(post):
							try:
								if(request.data["commentSno"]=="-1"):
									comment = BlogComment(user=user, post=post, comment=commentBody)
									comment.save()
									return Response({"success":"Comment Added Succesfully"})
								else:
									commentSno = int(request.data["commentSno"])
									parentComment = BlogComment.objects.get(sno=commentSno)
									comment = BlogComment(user=user, post=post, parent=parentComment,comment=commentBody)
									comment.save()
									return Response({"success":"Reply Added Succesfully"})
							except Exception as e:
								return Response({"error":"Internal server error!"})
						else:
							return Response({"error":"Post not found!"})
					else:
						return Response({"error":"User not found!"})
				except Exception as e:
					print(e)
					return Response({"error":"Internal servor error!"})
			else:
				return Response({"error":f"Fields not provided!"})
		except Exception as e:
			print(e)
			return Response({"error":"Internal Server Error"})