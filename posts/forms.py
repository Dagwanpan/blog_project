from django import forms 
from .models import Post

# Post form
class PostForm(forms.ModelForm):
    model = Post
    fields = [
        'title',
        'content'
    ]