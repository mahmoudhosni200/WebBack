from django.shortcuts import render
from .models import Member

# def is_admin(user):
#     return user.is_staff or user.is_superuser



def admin_profile(request):
    return render(request, 'Books/profileAdmin.html', {'admin': request.user})

# def user_profile(request):
#     return render(request, 'Books/profileUser.html', {'user': request.user})
from django.shortcuts import render
from information.models import Member

def user_profile(request):
    # dummy example
    member = Member(
        name='Jane Doe',
        email='jane@example.com',
        # profile_picture='image/boy.jpg'
    )
    return render(request, 'Books/profileUser.html', {'member': member})

