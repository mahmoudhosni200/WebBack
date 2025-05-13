document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("addBookForm");
    const fileNameSpan = document.getElementById("file-name");
    const imageInput = document.getElementById("book_image");

    imageInput.addEventListener("change", function () {
        fileNameSpan.textContent = imageInput.files[0]?.name || "No file chosen";
    });

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch("/api/books/add/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        })
        .then(response => {
            if (response.ok) {
                alert("Book added successfully!");
                form.reset();
                fileNameSpan.textContent = "No file chosen";
            } else {
                return response.json().then(data => {
                    alert("Error: " + (data.detail || "Failed to add book."));
                });
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Error adding book.");
        });
    });
});

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
