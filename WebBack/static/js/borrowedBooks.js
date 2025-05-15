
function getCsrfToken() {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
}

// Escape text to prevent XSS
function escapeHtml(unsafe) {
  if (!unsafe) return '';
  return unsafe
    .toString()
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Fetch and render borrowed books into .borrowed-list
function displayBorrowedBooks() {
  const container = document.querySelector('.borrowed-list');
  if (!container) return;

  container.innerHTML = '<h2>Your Borrowed Books</h2><hr>';

  fetch('/books/api/borrowed-books/')
    .then(res => {
      if (!res.ok) throw new Error('Network response was not ok');
      return res.json();
    })
    .then(books => {
      if (books.length === 0) {
        container.innerHTML += '<p>You have no borrowed books.</p>';
        return;
      }

      books.forEach(book => {
        const html = `
          <div class="container">
            <div class="img-item">
              <img src="${escapeHtml(book.imageSrc)}" alt="${escapeHtml(book.title)}">
            </div>
            <div class="item">
              <h3>${escapeHtml(book.title)}</h3>
              <h4>${escapeHtml(book.author)}</h4>
              <p>${escapeHtml(book.description)}</p>
            </div>
            <div class="book">
              <button onclick="returnBook(${book.bookId})" class="return-btn">Return Book</button>
            </div>
            <div class="clr"></div>
            <hr>
          </div>
        `;
        container.insertAdjacentHTML('beforeend', html);
      });
    })
    .catch(err => {
      console.error('Error fetching borrowed books:', err);
      container.innerHTML += '<p>An error occurred while loading borrowed books.</p>';
    });
}

// Send return request, then refresh
function returnBook(bookId) {
  fetch(`/books/api/return-book/${bookId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCsrfToken(),
      'Content-Type': 'application/json'
    }
  })
    .then(res => {
      if (!res.ok) throw new Error('Failed to return book');
      return res.json();
    })
    .then(json => {
      if (json.success) displayBorrowedBooks();
      else alert(json.message || 'Could not return the book.');
    })
    .catch(err => {
      console.error('Error returning book:', err);
      alert('An error occurred while returning the book.');
    });
}

// Initialize on DOM ready
window.addEventListener('DOMContentLoaded', displayBorrowedBooks);
