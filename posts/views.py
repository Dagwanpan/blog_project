from django.shortcuts import render, redirect, get_object_or_404
from .model import Post
from .form import PostForm

# Home page
def home(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {
        'posts': posts
    })
