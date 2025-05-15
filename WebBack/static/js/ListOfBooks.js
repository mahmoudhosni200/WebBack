

function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue;
}


function displayBooks() {
    const englishBooksContainer = document.querySelector('.english-books');
    const arabicBooksContainer = document.querySelector('.arabic-books');
    
    if (!englishBooksContainer || !arabicBooksContainer) return;
    
    loadBooks('english', englishBooksContainer);
    loadBooks('arabic', arabicBooksContainer);
}

function loadBooks(language, container) {
    fetch(`/books/api/books/?language=${language}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error fetching ${language} books`);
            }
            return response.json();
        })
        .then(books => {
            displayBooksInContainer(books, container);
        })
        .catch(error => {
            console.error('Error:', error);
            container.innerHTML += '<p style="color:red;">Error loading books.</p>';
        });
}

function displayBooksInContainer(books, container) {
    
    const categoryHeader = container.querySelector('h2');
    container.innerHTML = '';
    if (categoryHeader) {
        container.appendChild(categoryHeader);
    }
    
    if (!books.length) {
        container.innerHTML += '<p>No books available at the moment.</p>';
        return;
    }

    const fragment = document.createDocumentFragment();

    books.forEach(book => {
        const bookElement = document.createElement('div');
        bookElement.className = 'container';
        
        bookElement.innerHTML = `
            <div class="img-item">
                <img src="${escapeHtml(book.imageSrc || '/static/default_book.jpg')}" alt="${escapeHtml(book.title)}">
            </div>
            <div class="item">
                <h3>${escapeHtml(book.title)}</h3>
                <h4>Author: ${escapeHtml(book.author)}</h4>
                <p data-book-id="${book.id}">${escapeHtml(book.description)}</p>
            </div>
            <div class="book">
                <h3>Available copies: ${book.available}</h3>
                <button type="button" class="borrow-btn" onclick="borrowBook(this)" ${book.available <= 0 ? 'disabled' : ''}>
                    ${book.available > 0 ? 'Borrow' : 'Unavailable'}
                </button>
            </div>
            <div class="clr"></div>
            <hr>
        `;

        fragment.appendChild(bookElement);
    });

    container.appendChild(fragment);
}

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe.toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function borrowBook(button) {
    const bookContainer = button.closest('.container');
    const bookId = bookContainer.querySelector('[data-book-id]')?.getAttribute('data-book-id');

    if (!bookId) {
        alert("Book ID not found.");
        return;
    }

    const csrfToken = getCsrfToken();

    fetch(`/books/api/borrow-book/${bookId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Error borrowing the book');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Book borrowed successfully!');
            displayBooks();
        } else {
            alert(data.message || 'Could not borrow the book.');
        }
    })
    .catch(error => {
        console.error('Error borrowing the book:', error);
        alert(error.message || 'Error attempting to borrow the book. Please try again.');
    });
}


function displayBorrowedBooks() {
    const borrowedBooksContainer = document.querySelector('.borrowed-books');
    
    if (!borrowedBooksContainer) return;
    
    fetch('/books/api/borrowed-books/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error fetching borrowed books');
            }
            return response.json();
        })
        .then(books => {
            if (!books.length) {
                borrowedBooksContainer.innerHTML = '<p>You have not borrowed any books yet.</p>';
                return;
            }

            const fragment = document.createDocumentFragment();

            books.forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.className = 'container';
                
                bookElement.innerHTML = `
                    <div class="img-item">
                        <img src="${escapeHtml(book.imageSrc || '/static/default_book.jpg')}" alt="${escapeHtml(book.title)}">
                    </div>
                    <div class="item">
                        <h3>${escapeHtml(book.title)}</h3>
                        <h4>Author: ${escapeHtml(book.author)}</h4>
                        <p>${escapeHtml(book.description)}</p>
                    </div>
                    <div class="book">
                        <button type="button" class="return-btn" onclick="returnBook(${book.bookId})">Return Book</button>
                    </div>
                    <div class="clr"></div>
                    <hr>
                `;

                fragment.appendChild(bookElement);
            });

            borrowedBooksContainer.innerHTML = '';
            borrowedBooksContainer.appendChild(fragment);
        })
        .catch(error => {
            console.error('Error:', error);
            borrowedBooksContainer.innerHTML = '<p style="color:red;">Error loading borrowed books.</p>';
        });
}

function returnBook(bookId) {
    const csrfToken = getCsrfToken();

    fetch(`/books/api/return-book/${bookId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || 'Error returning the book');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Book returned successfully!');
            displayBorrowedBooks();
        } else {
            alert(data.message || 'Could not return the book.');
        }
    })
    .catch(error => {
        console.error('Error returning the book:', error);
        alert(error.message || 'Error attempting to return the book. Please try again.');
    });
}


window.onload = function() {
    
    if (document.querySelector('.english-books') || document.querySelector('.arabic-books')) {
        displayBooks();
    } else if (document.querySelector('.borrowed-books')) {
        displayBorrowedBooks();
    }
};