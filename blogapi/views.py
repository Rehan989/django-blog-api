from django.shortcuts import render

# Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response

from userauthapi.serializers import User

# Imports from Serializer
from .serializers import PostSerializer,CommentSerializer

# Models impor
from .models import Post, BlogComment, Contact

from rest_framework import permissions
from rest_framework.decorators import (
    permission_classes,
)
from django.db.models import Min

# Method for fetching LatestBlogPosts
class LatestBlogPosts(APIView):
	def get(self, request, format=None):
		try:
			# Extracting Page Size from get body
			pageSize = request.GET['pageSize']
			# blogPosts = Post.objects.all().exclude(publish_state="draft")[0:int(pageSize)]
			blogPosts = Post.objects.order_by('-last_updated').exclude(publish_state="draft")[0:int(pageSize)]
			serializer = PostSerializer(blogPosts, many=True)
			# Returning Parsed Posts
			return Response({"posts":serializer.data, "success":"Success!"})
		except KeyError:
			# blogPosts = Post.objects.all().exclude(publish_state="draft")[0:6]
			blogPosts = Post.objects.order_by('-last_updated').exclude(publish_state="draft")[0:6]
			serializer = PostSerializer(blogPosts, many=True)
			# Return 6 latest Parsed posts if pageSize is not provided
			return Response({"posts":serializer.data, "success":"Success!"})
		except Exception as e:
			print(e)
			return Response({"error":"Internal Server Error"})


# Method for fetching Blogposts Through page Number
class BlogPosts(APIView):
	def get(self, request, pageNumber, format=None):
		try:
			# Defining pageSize of all the pages
			pageSize = 8
			if(pageNumber>=0):
				try:
					# Returning the bloposts according to blog page and pageSize
					blogPosts = Post.objects.order_by('-last_updated').exclude(publish_state="draft")[pageNumber*8:pageNumber*8+8]
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
class FetchBlogPost(APIView):
	def get(self, request, slug, format=None):
		try:
			# Extracting Page Size from get body
			if(slug):
				post = Post.objects.get(slug=slug)
				postSerializer = PostSerializer(post)
				# Returning Parsed Post
				return Response({"post": postSerializer.data, "success":"Blog found Successfully"})
			else:
				return Response({"error":"Not found!"})
		except Exception as e:
			print(e)
			return Response({"error":"Internal Server Error"})

class FetchComments(APIView):
	def get(self, request, slug, format=None):
		try:
			# Extracting Page Size from get body
			if(slug):
				post = Post.objects.get(slug=slug)
				comments = BlogComment.objects.filter(post=post)
				commentSerializer = CommentSerializer(comments, many=True)
				for commentSerial, comment in zip(commentSerializer.data, comments):
					commentSerial['user'] = str(comment.user)
				# Returning Parsed Post
				return Response({"comments":commentSerializer.data, "success":"Blog found Successfully"})
			else:
				return Response({"error":"Not found!"})
		except Exception as e:
			print(e)
			return Response({"error":"Internal Server Error"})


# Method for Adding likes to blog post
@permission_classes([permissions.IsAuthenticated])
class Addlike(APIView):
	def put(self, request, format=None):
		try:
			# Extracting Page Size from get body
			# Change all this type of clutters with token Authorization
			email = request.user.email
			username = request.user.username
			postSno = request.data['sno']
			if(email, username):
				try:
					user = User.objects.get(email=email, username=username)
					if(user):
						post = Post.objects.get(sno=postSno)
						if(post):
							post.likes.add(user)
							post.save()
							return Response({"success":f"Updated Succesfully! Total likes: {post.total_likes()}"})
						else:
							return Response({"error":"Post not found!"})
					else:
						return Response({"error":"User not found!"})
				except Exception as e:
					print(e)
					return Response({"error":"Internal servor error!"})
		except KeyError as e:
			print(e)
			return Response({"error":"Fields not provided!"})
		except Exception as e:
			print(e)
			return Response({"error":"Internal Server Error"})


# Method for Removing likes from blog post
@permission_classes([permissions.IsAuthenticated])
class RemoveLike(APIView):
	def post(self, request, format=None):
		try:
			# Extracting Page Size from get body
			email = request.user.email
			username = request.user.username
			postSno = request.data['sno']
			if(email, username):
				try:
					user = User.objects.get(email=email, username=username)
					if(user):
						post = Post.objects.get(sno=postSno)
						if(post):
							post.likes.remove(user)
							post.save()
							return Response({"success":f"Updated Succesfully! Total likes: {post.total_likes()}"})
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


# Method for Adding comments to blog post
@permission_classes([permissions.IsAuthenticated])
class AddComment(APIView):
	def post(self, request, format=None):
		try:
			# Extracting Required values from get body
			email = request.user.email
			username = request.user.username
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
								print(e)
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




class SearchPost(APIView):
	def get(self, request, format=None):
		try:
			query=request.GET['query']
			print(query)
			if len(query)>8:
				allPosts = Post.objects.none()
			else:
				allPostsTitle = Post.objects.filter(title__icontains=query).exclude(publish_state="draft")
				allPostsAuthor = Post.objects.filter(author__icontains=query).exclude(publish_state="draft")
				allPostsContent = Post.objects.filter(content__icontains=query).exclude(publish_state="draft")
				allPosts = allPostsTitle.union(allPostsAuthor, allPostsContent)
			serializer = PostSerializer(allPosts, many=True)
			return Response({"results":serializer.data, "success":True})
		except Exception as e:
			return Response({"error":"Internal Server Error"})


@permission_classes([permissions.IsAuthenticated])
class AddContact(APIView):
	def put(self, request, format=None):
		try:
			email = request.user.email
			username = request.user.username
			contactBody = request.data['contactBody']
			contact = Contact(email=email,name=username,contactBody=contactBody)
			contact.save()
			return Response({"success":"Contact form submitted successfully"})
		except Exception as e:
			print(e)
			return Response({"error":"Internal Server Error"})