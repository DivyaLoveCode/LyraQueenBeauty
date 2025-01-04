// Function to toggle the menu visibility
function toggleMenu() {
    const navLinks = document.getElementById('nav-links');
    // Toggle the visibility of the menu
    if (navLinks.style.display === 'block') {
        navLinks.style.display = 'none';
    } else {
        navLinks.style.display = 'block';
    }
}
