from django.shortcuts import render, redirect, get_object_or_404
from .model import Post
from .form import PostForm

# Home page
def home(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {
        'posts': posts
    })
    
# Creat post
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'posts/create_post.html', {
        'form': form
    })