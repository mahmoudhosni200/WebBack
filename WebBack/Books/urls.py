from django.urls import path
from . import views
urlpatterns=[
    path('AddBook/', views.addBook, name='addBook'),
    path('ListAdmin/', views.list_books_admin, name='list_books_admin'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]