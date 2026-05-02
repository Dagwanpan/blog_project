from django import forms 
from .models import Post, Comment

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