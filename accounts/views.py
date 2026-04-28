from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm

# Registration form
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {
        'form': form
    })

# Logout User
def logout_user(request):
    logout(request)
    return redirect('home')