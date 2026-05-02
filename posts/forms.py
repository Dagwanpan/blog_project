from django import forms 
from .models import Post

# Post form
class PostForm(forms.ModelForm):    
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image'
        ]