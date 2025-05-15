from django.urls import path
from . import views

urlpatterns = [
    # path('', views.profile_view, name='profile'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),
    path('user/profile/', views.user_profile, name='user_profile'),
    
]
