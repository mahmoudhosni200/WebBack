
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Book, BorrowedBook
# from django.contrib.auth.models import AnonymousUser
import uuid


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


def borrowed_books(request):
    """Display the borrowed books page"""
    if not request.session.get('session_id'):
        request.session['session_id'] = str(uuid.uuid4())
    return render(request, 'books/borrowedBooks.html')

def get_borrowed_books(request):
    session_id = request.session.get('session_id')
    if not session_id:

        return JsonResponse([], safe=False)
    
    borrowed_books = BorrowedBook.objects.filter(session_id=session_id).select_related('book')
    
    books_list = []
    for borrowed_book in borrowed_books:
        book = borrowed_book.book
        books_list.append({
            'bookId': book.id,
            'title': book.book_name,
            'author': book.author,
            'description': book.description,
            'imageSrc': book.book_image.url if book.book_image else '/static/images/default.jpg',
        })
    return JsonResponse(books_list, safe=False)

def return_book(request, book_id):
    """Return a borrowed book"""
    if request.method == 'POST':
        session_id = request.session.get('session_id')
        if not session_id:
            return JsonResponse({'success': False, 'message': 'No borrowed books found.'}, status=400)
        
        book = get_object_or_404(Book, id=book_id)
        
        try:
            borrowed_book = BorrowedBook.objects.get(session_id=session_id, book=book)
            
            
            book.available_copies += 1
            book.borrowed_copies -= 1
            book.save()
            
        
            borrowed_book.delete()
            
            return JsonResponse({'success': True})
        except BorrowedBook.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'You have not borrowed this book.'}, status=400)
    
    return JsonResponse({'success': False}, status=400)


def borrow_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        if book.available_copies <= 0:
            return JsonResponse({'success': False, 'message': 'This book is currently unavailable.'}, status=400)
        
    
        if not request.session.get('session_id'):
            request.session['session_id'] = str(uuid.uuid4())
        session_id = request.session.get('session_id')
        
        
        if BorrowedBook.objects.filter(session_id=session_id, book=book).exists():
            return JsonResponse({'success': False, 'message': 'You have already borrowed this book.'}, status=400)
        
        
        book.available_copies -= 1
        book.borrowed_copies += 1
        book.save()
        
        
        if request.user.is_authenticated:
            BorrowedBook.objects.create(user=request.user, book=book, session_id=session_id)
        else:
            BorrowedBook.objects.create(user=None, book=book, session_id=session_id)
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


def list_books(request):
    """Display the book list page"""
    return render(request, 'books/ListUser.html')


def get_books(request):
    """API endpoint to retrieve the list of books"""
    language = request.GET.get('language', 'all')
    
    if language == 'english':
        books = Book.objects.filter(language='english')
    elif language == 'arabic':
        books = Book.objects.filter(language='arabic')
    else:
        books = Book.objects.all()
    
    books_list = []
    for book in books:
        books_list.append({
            'id': book.id,
            'title': book.book_name,
            'author': book.author,
            'description': book.description,
            'imageSrc': book.book_image.url if book.book_image else '/static/images/default.jpg',
            'available': book.available_copies,
            'borrowed': book.borrowed_copies,
        })
    
    return JsonResponse(books_list, safe=False)
