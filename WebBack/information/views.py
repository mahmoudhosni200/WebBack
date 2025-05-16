from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Member

# Register (Sign Up)
def sign_up_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email    = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully')
        return redirect('signin')
    return render(request, 'information/signUp.html')

# Login (Sign In)
def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
              
            if user.is_staff or user.is_superuser:
                return redirect('admin_profile')
            else:
                return redirect('user_profile')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')

    return render(request, 'information/signIn.html')

#  Logout
def logout_view(request):
    logout(request)
    return redirect('signin')

#login_required
def admin_profile(request):
    return render(request, 'Books/profileAdmin.html', {'admin': request.user})

#login_required
def user_profile(request):
    return render(request, 'Books/profileUser.html', {'member': request.user})


#  Optional index page
def index_view(request):
    return render(request, 'information/index.html')


