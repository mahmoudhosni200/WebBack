from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('AdminHome/', views.homeAdmin_view, name='homeAdmin'),
    path('signup/', views.sign_up_view, name='signup'),
    path('signin/', views.sign_in_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('adminProfile/', views.admin_profile, name='admin_profile'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/authunticate/', views.authenticate_member, name='authenticate_user'),
    path('contact/', views.contact_view, name='contact'),

]

