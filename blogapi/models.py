from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.utils.timezone import now
from io import BytesIO
from PIL import Image
from django.core.files import File

# Image compression
def compress(image):
    im = Image.open(image)
    im = im.convert('RGB')
    # create a BytesIO object
    im_io = BytesIO() 
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=25,optimize=True) 
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image

# Method for adding Likes to the Post
class Likes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)


# Blog Posts Model
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=55)
    slug = models.CharField(max_length=130)
    views = models.IntegerField(default=0)
    content = models.TextField()
    last_updated = models.DateTimeField(blank=True)
    meta_description = models.CharField(max_length=500)
    publish_state = models.CharField(max_length=10, choices=(('publish', 'PUBLISH'), ('draft', 'DRAFT')))
    featured_image = models.ImageField(upload_to='blog/image/', default="")
    likes = models.ManyToManyField(Likes, blank=True)


    def save(self, *args, **kwargs):
        if self.featured_image:
            new_img = compress(self.featured_image)
            self.featured_image = new_img
            super().save(*args, **kwargs)
    def __str__(self):
        return self.title


# ManytoManyfield for storing the users bookmarked posts
class Bookmarks(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

# Blogs Comments Model
class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)
    bookmarks = models.ManyToManyField(Bookmarks, blank=True)

    def __str__(self):
        return self.comment[0:13] + '...' + " by " + self.user.username