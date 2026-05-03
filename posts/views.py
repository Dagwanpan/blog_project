from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Home page
def home(request):
    posts = Post.objects.select_related('user').prefetch_related(
        'comments').annotate(
        total_comments=Count('comments')
    ).order_by('-created_at')
        
    return render(request, 'posts/home.html', {
        'posts': posts
    })
    
# Creat post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(f'/post/{post.id}/#create_post')
    else:
        form = PostForm()
    
    return render(request, 'posts/create_post.html', {
        'form': form
    })

# Update post by id
@login_required
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    
    if post.user != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        
        if form.is_valid():
            form.save()
            return redirect(f'/post/{post.id}/#update_post')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/update_post.html', {
        'form': form
    })

# Display Post detail by id
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    
    if request.method == 'POST':
        
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user 
            
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            
            comment.save()
            
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()
        
    comments = post.comments.select_related('user').filter(
        parent=None
    ).order_by('-created_at')
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })
    
# Edit comment
@login_required
def edit_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    
    if comment.user != request.user:
        return redirect('login')
    
    if request.method == 'POST':
        
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(f'/post/{comment.post.id}/#comments')
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'posts/edit_comment.html', {
        'form': form
    })

# Delete comment by id
@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    
    if comment.user != request.user:
        return redirect('login')
    
    if request.method =='POST':
        post_id = comment.post.id
        comment.delete()
        
        return redirect(f'/post/{post_id}#comments')     

# Delete post by Id
@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    
    if post.user != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        
    return redirect('home')