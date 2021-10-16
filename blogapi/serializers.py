from rest_framework import serializers
from .models import Post, BlogComment

# Post serializer for showing details as described 
class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = (
			'sno',
			"title",
			"author",
			"slug",
			"views",
			"content",
			"last_updated",
			"meta_description",
			"publish_state",
			"featured_image",
			"likes"
		)



# Comment serializer for showing details as described 
class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogComment
		fields = (
			'sno',
			"comment",
			"user",
			"post",
			"parent",
			"timestamp",
		)