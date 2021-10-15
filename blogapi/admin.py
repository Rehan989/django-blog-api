from django.contrib import admin
from .models import Post, BlogComment
# Models Reigistration

admin.site.register((BlogComment))

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('js/tiny_mce.js',)
