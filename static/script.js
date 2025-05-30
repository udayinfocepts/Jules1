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

// --- Toast Notification Functionality ---
function showToast(message, type = 'error', duration = 5000) {
    const container = document.getElementById('toastContainer');
    if (!container) {
        console.error('Toast container not found!');
        return;
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`; // e.g., toast-error, toast-success
    toast.textContent = message;

    container.appendChild(toast);

    // Trigger reflow for animation
    toast.offsetHeight; 

    // Add class to make it visible and animate
    toast.classList.add('show');

    // Remove toast after specified duration
    setTimeout(() => {
        toast.classList.remove('show');
        // Remove the element from DOM after animation
        setTimeout(() => {
            if (toast.parentNode === container) { // Check if still child before removing
                container.removeChild(toast);
            }
        }, 500); // Matches CSS transition time
    }, duration);
}
