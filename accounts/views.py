from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm

# Register Form.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'accouts/register.html', {
        'form': form        
    })

# Logout user
def logout_user(request):
    logout(request)
    return reidrec('home')