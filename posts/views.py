from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# Home page
def home(request):
    posts = Post.objects.all()
    
    return render(request, 'posts/home.html', {
        'posts': posts
    })

# Create Post
@login_required
def create_post(request):
    if request.method == 'POST': 
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
        
    return render(request, 'posts/create_post.html', {
        'form': form
    })
    
# Update Post by id
@login_required
def update_post(request, id): 
    post = get_object_or_404(Post, id=id)
    
    if post.author != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/update_post.html', {
        'form': form
    })
    
# Display all post by id
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    
    return render(request, 'posts/post_detail.html', {
        'post': post
    })

# Delete post by id
@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    
    if post.author != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
    return render(request, 'posts/delete_post.html', {
        'post': post
    })