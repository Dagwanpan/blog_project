from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm, ProfileForm, UserUpdateForm

# Home page
def home(request):
    posts = Post.objects.select_related(
        'author'
        ).prefetch_related(
        'comments'
        ).annotate(
        total_comments=Count(
            'comments'
            )
    ).order_by(
        '-created_at'
        )
        
    return render(request, 'posts/home.html', {
        'posts': posts
    })

# Profile Page
@login_required
def profile(request):
    
    profile = request.user.profile
    
    if request.method ==  'POST':
        
        # Profile form
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        
        # User Form
        user_form = UserUpdateForm(
            request.user,
            instance=request.user
        )
        
        # Password Form
        password_form = PasswordChangeForm(
            request.user,
            request.POST
        )
        
        # Update profile + username/email
        if 'update_profile' in request.POST:
            
            if profile_form.is_valid() and user_form.is_valid():
                profile_form.save()
                user_form.save()
                return redirect('profile')
        
        # Change password
        elif 'change_password' in request.POST:
            
            if password_form.is_valid():
                
                user = password_form.save()
                
                # Important: keep user logged in
                update_session_auth_hash(request, user)
        
        # Delete user account
        elif 'delete_account' in request.POST:
            
            user = request.user
            
            logout(request)
            
            user.delete()
            return redirect('profile')
    
    else:
        profile_form = ProfileForm(instance=profile)
        
        user_form = UserUpdateForm(instance=request.user)
        
        password_form = PasswordChangeForm(request.user)
    
    user_posts = request.user.post_set.all()
    
    user_comments = request.user.comment_set.all()
    
    return render(request, 'posts/profile.html', {
        'profile_form': profile_form,
        'user_form': user_form,
        'password_form': password_form,
        'profile': profile,
        'user_posts': user_posts,
        'user_comments': user_comments
    })
        
# Create post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
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
    
    if post.author != request.user:
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
            comment.author = request.user 
            
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            
            comment.save()
            
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()
        
    comments = post.comments.select_related(
        'author'
        ).filter(
        parent=None
    ).order_by(
        '-created_at'
        )
    
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })
    
# Edit comment
@login_required
def edit_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    
    if comment.author != request.user:
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
    
    if comment.author != request.user:
        return redirect('login')
    
    if request.method =='POST':
        post_id = comment.post.id
        comment.delete()
        
        return redirect(f'/post/{post_id}#comments')     

# Delete post by Id
@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    
    if post.author != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        
    return redirect('home')