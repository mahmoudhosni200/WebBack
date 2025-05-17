from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model

Member = get_user_model()

# ✅ SIGN UP VIEW
def sign_up_view(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        user_type = request.POST.get('choice')

        if Member.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        try:
            user = Member.objects.create_user(email=email, name=name, password=password)

            if user_type == 'option1':  # Admin checkbox or radio
                user.is_staff = True
            user.save()

            messages.success(request, 'Account created successfully')
            return redirect('signin')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('signup')

    return render(request, 'information/signUp.html')

# ✅ SIGN IN VIEW
def sign_in_view(request):
    if request.method == 'POST':
        name = request.POST['username']  # or change to `email` if form uses that
        password = request.POST['password']

        user = authenticate_member(name=name, password=password)
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

# ✅ CUSTOM AUTH FUNCTION
def authenticate_member(name, password):
    try:
        user = Member.objects.get(name=name)
        if user.check_password(password):
            return user
    except Member.DoesNotExist:
        return None
    return None

# ✅ LOGOUT
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


def homeAdmin_view(request):
    return render(request, 'information/homeAdmin.html')