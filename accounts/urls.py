from django.urls import path
from django.contrib.auth import views as auth_view
from .views import register, logout_user

# Registration urls routes
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
]
