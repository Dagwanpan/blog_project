from django import forms 
from .model import Post

# Post form
class PostForm(forms.ModelForm):
    model = Post
    fields = [
        'title',
        'content'
    ]