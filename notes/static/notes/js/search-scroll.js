document.addEventListener('DOMContentLoaded', function () {
    // Select the elements
    const searchButton = document.querySelector('#searchButton');
    const searchInput = document.querySelector('#search');
    const alertContainer = document.getElementById("no-results-alert");
    const createNoteLink = document.querySelector('#create-note-link');

    // Check if the elements exist
    if (searchButton && searchInput && alertContainer) {
        searchButton.addEventListener('click', function () {
            const searchQuery = searchInput.value.trim();

            // Show or hide the alert based on the search query
            if (searchQuery) {
                // Perform an actual search and check if results are found
                // For now, assuming if no note items exist, it shows no results alert
                if (document.querySelector('.note-item')) {
                    alertContainer.classList.add('hide'); // Hide the alert if there are results
                } else {
                    alertContainer.classList.remove('hide');
                    alertContainer.classList.add('show'); // Show alert if no results
                }
            } else {
                alertContainer.classList.remove('hide'); // Show alert if input is empty
                alertContainer.classList.add('show');
            }
        });
    }

    // Clear the search input and reset the URL query when navigating to "Create Note" page
    if (createNoteLink) {
        createNoteLink.addEventListener('click', function () {
            if (searchInput) {
                searchInput.value = ''; // Clear the search input
            }

            // Reset URL by removing the search query parameter
            const currentURL = new URL(window.location.href);
            currentURL.searchParams.delete('search');  // Remove search query parameter
            window.history.replaceState({}, '', currentURL);  // Update URL without reloading the page
        });
    }

    // Optional: Clear search input when the page loads for create-note page
    if (window.location.href.includes('create_note') && searchInput) {
        searchInput.value = '';
    }
});
