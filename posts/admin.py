from django.contrib import admin
from .models import Post, Comment

# Register Models.
admin.site.register(Post)
admin.site.register(Comment)