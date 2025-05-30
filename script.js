function openTab(event, tabName) {
    // Declare all variables
    var i, tabcontent, tabbuttons;

    // Get all elements with class="tab-content" and hide them
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        tabcontent[i].classList.remove("active"); // Remove active class from content
    }

    // Get all elements with class="tab-button" and remove the class "active"
    tabbuttons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].classList.remove("active");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab and its content
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabName).classList.add("active");
    event.currentTarget.classList.add("active");
}

// Ensure the default tab is displayed on page load
document.addEventListener('DOMContentLoaded', (event) => {
    // Check if any tab button is already marked active in HTML (e.g. ChatGPT)
    // If not, or to be certain, click the first tab button by default.
    // This assumes 'chatgpt' is the ID of the first tab's content and
    // the first button corresponds to it.
    const defaultActiveButton = document.querySelector('.tab-button.active');
    if (defaultActiveButton) {
        defaultActiveButton.click(); // Trigger click to ensure content is shown
    } else {
        // Fallback if no button is pre-marked as active (should not happen with current HTML)
        document.querySelector('.tab-button').click();
    }
});
