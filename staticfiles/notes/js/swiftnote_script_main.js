document.addEventListener('DOMContentLoaded', function () {
    // Select success message containers
    const successMessages = document.querySelectorAll('.alert-success');

    // Only handle error messages on pages that are not 'create_note'
    const errorMessages = document.querySelectorAll('.alert-danger');
    const currentPage = window.location.pathname;  // Get the current URL path

    // Function to hide a message after a timeout
    function hideMessage(message, timeout) {
        setTimeout(function () {
            message.style.display = 'none';  // Hide the message
        }, timeout);  // Timeout specified in milliseconds
    }

    // Hide success messages
    successMessages.forEach(function (message) {
        if (message.textContent.includes('Note created successfully!')) {
            hideMessage(message, 10000); // 10 seconds for note creation success message
        } else {
            hideMessage(message, 5000); // 5 seconds for other success messages
        }
    });

    // Only hide error messages on pages where they are needed (not on 'create_note')
    if (!currentPage.includes('create_note')) {
        errorMessages.forEach(function (message) {
            hideMessage(message, 5000);  // 5 seconds for error messages
        });
    }
});
