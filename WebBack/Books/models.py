
#  from django.contrib.auth.models import User

# # Create your models here.

# class Book(models.Model):
#     LANGUAGE_CHOICES = [
#         ('english', 'English'),
#         ('arabic', 'Arabic'),
#     ]

#     book_name = models.CharField(max_length=200)
#     author = models.CharField(max_length=200)
#     category = models.CharField(max_length=100)
#     description = models.TextField()
#     available_copies = models.PositiveIntegerField()
#     borrowed_copies = models.PositiveIntegerField(default=0)
#     language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
#     book_image = models.ImageField(upload_to='book_images/')

# # class Book(models.Model):
# #     title = models.CharField(max_length=200)
# #     author = models.CharField(max_length=200)
# #     description = models.TextField()
# #     image = models.ImageField(upload_to='book_images/', null=True, blank=True)
# #     available = models.IntegerField(default=1)
# #     borrowed = models.IntegerField(default=0)
    
# #     def __str__(self):
# #         return self.title

# class BorrowedBook(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     borrow_date = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.user.username} - {self.book.book_name}"

from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('arabic', 'Arabic'),
    ]
    
    book_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    available_copies = models.PositiveIntegerField()
    borrowed_copies = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    book_image = models.ImageField(upload_to='book_images/')
    
    def __str__(self):
        return self.book_name

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.book.book_name} borrowed by {self.user or self.session_id}"