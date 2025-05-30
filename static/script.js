document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('apiStatusModal');
    const openModalButton = document.getElementById('openApiStatusModal');
    const closeModalButton = document.getElementsByClassName('close-modal-button')[0];

    if (openModalButton) {
        openModalButton.onclick = function() {
            if (modal) modal.style.display = 'block';
        }
    }

    if (closeModalButton) {
        closeModalButton.onclick = function() {
            if (modal) modal.style.display = 'none';
        }
    }

    // Optional: Close modal if user clicks outside of the modal content
    window.onclick = function(event) {
        if (event.target == modal) {
            if (modal) modal.style.display = 'none';
        }
    }
});
