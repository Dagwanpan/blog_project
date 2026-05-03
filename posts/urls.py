from django.urls import path 
from .views import home, create_post, update_post, post_detail, delete_post, edit_comment, delete_comment

# Post url routes
urlpatterns = [
    path('', home, name='home'),
    path('create/', create_post, name='create_post'),
    path('update/<int:id>/', update_post, name='update_post'),
    path('post/<int:id>/', post_detail, name='post_detail'),
    path('delete/<int:id>/', delete_post, name='delete_post'),
    path('edit/comment/<int:id>/', edit_comment, name='edit_comment'),
    path('delete/comment/<int:id>/', delete_comment, name='delete_comment'),
]
