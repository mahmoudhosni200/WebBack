from django.shortcuts import render, redirect, reverse
from .models import Book
from django.http import HttpResponse


# Create your views here.
def addBook(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        
        if 'book_image' in request.FILES:
            book = Book(
                book_name=request.POST['book_name'],
                author=request.POST['author'],
                category=request.POST['category'],
                description=request.POST['description'],
                available_copies=request.POST['available_copies'],
                language=request.POST['choice'],
                book_image=request.FILES['book_image']
            )
            book.save()
            return redirect('list_books_admin')
        else:
            print("Error: Book image not found!")
    return render(request, 'Books/addBook.html')


# def list_books_admin(request):
#     if request.method == 'GET':
#         english_books = Book.objects.filter(language='english')
#         arabic_books = Book.objects.filter(language='arabic')
#         return render(request, 'Books/ListAdmin.html', {
#             'english_books': english_books,
#             'arabic_books': arabic_books
#         })
def list_books_admin(request):
    english_books = Book.objects.filter(language='english')
    arabic_books = Book.objects.filter(language='arabic')
    return render(request, 'Books/ListAdmin.html', {
        'english_books': english_books,
        'arabic_books': arabic_books
    })
    
def delete_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.filter(id=book_id).first()
        if book:
            book.delete()

    english_books = Book.objects.filter(language='english')
    arabic_books = Book.objects.filter(language='arabic')
    
    return render(request, 'Books/ListAdmin.html', {
        'english_books': english_books,
        'arabic_books': arabic_books,
        'message': 'Book deleted successfully'
    })
def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.book_name = request.POST['book_name']
        book.author = request.POST['author']
        book.category = request.POST['category']
        book.description = request.POST['description']
        book.available_copies = request.POST['available_copies']
        book.language = request.POST['choice']
        
        if 'book_image' in request.FILES:
            book.book_image = request.FILES['book_image']
        
        book.save()
        return redirect('list_books_admin')
    
    return render(request, 'Books/Edit_Book.html', {'book': book})