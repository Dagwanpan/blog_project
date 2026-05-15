from django.contrib import admin
from .models import Post, Comment, Profile

# Register the apps.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)