document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('.contact-form');
    const formContainer = document.querySelector('.container');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');


    const confirmationContainer = document.createElement('div');
    confirmationContainer.className = 'confirmation-container';
    confirmationContainer.style.display = 'none'; 
    confirmationContainer.innerHTML = `
        <div class="confirmation-content">
            <i class="fa fa-check-circle confirmation-icon" aria-hidden="true"></i>
            <h3 class="confirmation-title">Thank You!</h3>
            <p class="confirmation-text">Your message has been received successfully.</p>
            <p class="confirmation-details">Our support team will get in touch with you within 24 hours.</p>
            <button class="confirmation-close-btn">OK</button>
        </div>
    `;
    
 
    formContainer.parentNode.insertBefore(confirmationContainer, formContainer.nextSibling);


    nameInput.addEventListener('input', validateName);
    emailInput.addEventListener('input', validateEmail);
    messageInput.addEventListener('input', validateMessage);

    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const isNameValid = validateName();
        const isEmailValid = validateEmail();
        const isMessageValid = validateMessage();

        if (isNameValid && isEmailValid && isMessageValid) {
        
            const submitBtn = document.querySelector('.contact-btn');
            submitBtn.innerHTML = '<i class="fa fa-spinner fa-spin"></i> Sending...';
            submitBtn.disabled = true;

            setTimeout(function() {
                
                formContainer.style.display = 'none';
                confirmationContainer.style.display = 'block';
                
                contactForm.reset();
                submitBtn.innerHTML = 'Send Message';
                submitBtn.disabled = false;
            }, 300);
        }
    });
    confirmationContainer.querySelector('.confirmation-close-btn').addEventListener('click', function() {
        confirmationContainer.style.display = 'none';
        formContainer.style.display = 'block';
    });

    function validateName() {
        const name = nameInput.value.trim();
        const isValid = name.length >= 3 && name.includes(' ');
        
        if (!isValid) {
            showError(nameInput, 'Please enter your full name (first and last name)');
            return false;
        }
        clearError(nameInput);
        return true;
    }

    function validateEmail() {
        const email = emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isValid = emailRegex.test(email);
        
        if (!isValid) {
            showError(emailInput, 'Please enter a valid email address');
            return false;
        }
        clearError(emailInput);
        return true;
    }

    function validateMessage() {
        const message = messageInput.value.trim();
        const isValid = message.length >= 10;
        
        if (!isValid) {
            showError(messageInput, 'Message must be at least 10 characters long');
            return false;
        }
        clearError(messageInput);
        return true;
    }

    function showError(input, message) {
        clearError(input);
        input.classList.add('error');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        input.parentNode.insertBefore(errorDiv, input.nextSibling);
    }

    function clearError(input) {
        input.classList.remove('error');
        const errorDiv = input.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('error-message')) {
            errorDiv.remove();
        }
    }
});
 