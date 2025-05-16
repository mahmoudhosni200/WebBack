# from django.db import models

# class Member(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, unique=True)
#     membership_date = models.DateField(auto_now_add=True)
#     membership_type = models.CharField(max_length=50)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

#     def __str__(self):
#         return self.name
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class MemberManager(BaseUserManager):
    def create_user(self, email, name, password = None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Member(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    # phone_number = models.CharField(max_length=15, unique=True)
    membership_date = models.DateField(auto_now_add=True)
    # membership_type = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    password = models.CharField(max_length=128, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password' ]

    def __str__(self):
        return self.name
