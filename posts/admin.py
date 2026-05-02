from django.contrib import admin
from .models import Post, Comment

# Register the app.
admin.site.register(Post)
admin.site.register(Comment)