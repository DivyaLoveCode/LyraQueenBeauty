
// Function to toggle cart visibility //
function toggleCart() {
    const cartSection = document.getElementById('cart-section');
    const currentDisplay = cartSection.style.display;

    console.log(`Current Display: ${currentDisplay}`); // Debugging line

    // Toggle cart visibility: if it's hidden, show it, else hide it
    if (currentDisplay === 'none' || currentDisplay === '') {
        cartSection.style.display = 'block';  // Show cart
    } else {
        cartSection.style.display = 'none';   // Hide cart
    }
}

// Add event listener to the cart icon (only once when DOM is loaded)
document.addEventListener('DOMContentLoaded', function () {
    const cartIcon = document.getElementById('cart-icon');
    
    if (cartIcon) {
        cartIcon.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent default anchor action
            toggleCart(); // Toggle cart visibility
        });
    }
});