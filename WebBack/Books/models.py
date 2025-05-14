from django.db import models

# Create your models here.

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
