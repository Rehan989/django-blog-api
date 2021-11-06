from django.contrib import admin
from .models import Post, BlogComment, Contact
# Models Reigistration

admin.site.register((BlogComment, Contact))

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('js/tiny_mce.js',)
