from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages

# Login views

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request=request, message='Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            group, _ = Group.objects.get_or_create(name='Viewer')
            user.groups.add(group)
            messages.success(request=request, message= "User created successfully")
            return redirect('login')
        return render(request, 'register.html')
    else:
        return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# Profile Views

@login_required
def user_profile(request):
    return render(request, 'profile.html',{
        'user': request.user
    })