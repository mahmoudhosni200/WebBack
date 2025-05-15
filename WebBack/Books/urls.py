from django.urls import path
from . import views
urlpatterns=[
    path('AddBook/', views.addBook, name='addBook'),
    path('ListAdmin/', views.list_books_admin, name='list_books_admin'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('Edit_Book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('ListUser/', views.list_books, name='ListUser'),
    path('borrowed-books/', views.borrowed_books, name='borrowed_books'),
    path('api/books/', views.get_books, name='get_books'),
    path('api/borrow-book/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('api/return-book/<int:book_id>/', views.return_book, name='return_book'),
    path('api/borrowed-books/', views.get_borrowed_books, name='get_borrowed_books'),
]