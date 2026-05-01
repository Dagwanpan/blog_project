from django.db import models

# Post model.
class Post(models.Model):
    title = models.CharFied(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_add_now=True)
    
    def __str__(self):
        return self.title
    