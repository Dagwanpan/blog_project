from django import forms 
from django.contrib.auth.models import User
from .models import Post, Comment, Profile

# Post form
class PostForm(forms.ModelForm):    
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image'
        ]

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = [
            'content',
            'image'
        ]    

# Profile Form
class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = [
            'bio',
            'image'
        ]  

# Profile User Update Form
class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]