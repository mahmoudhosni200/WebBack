document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("addBookForm");
    const fileNameSpan = document.getElementById("file-name");
    const imageInput = document.getElementById("book_image");

    imageInput.addEventListener("change", function () {
        fileNameSpan.textContent = imageInput.files[0]?.name || "No file chosen";
    });
});


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
