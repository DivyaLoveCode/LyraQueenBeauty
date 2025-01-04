console.log('cart.js loaded');

// Global cart array to store cart data temporarily
let cart = [];

// Function to load the cart from the session on page load
function loadCartFromSession() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');  // Use <meta> tag for CSRF

    fetch('/get-cart/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server Response:', data);  // Log full response for debugging

        // Check if data is valid and contains the cart property
        if (data && Array.isArray(data.cart)) {
            cart = data.cart;  // Use the cart array returned from the server
        } else {
            console.error('Error: Cart data is not an array:', data ? data.cart : 'No cart data');
            cart = [];  // Default to an empty array if data.cart is not an array
        }

        updateCart();  // Update the UI with the cart data
    })
    .catch(error => {
        console.error('Error loading cart:', error);  // Log fetch errors
    });
}

// Function to save the cart data to the session
function saveCartToSession(cart) {
    // Ensure the cart is an array before proceeding
    if (!Array.isArray(cart)) {
        console.error('Error: Cart is not an array. Data:', cart);
        return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch('/save-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Send the CSRF token correctly
        },
        body: JSON.stringify({ cart: cart })
    })
    .then(response => response.json()) // Parse the response as JSON
    .then(data => {
        // Check if the server response indicates success
        if (data && data.message && data.message === "Cart saved successfully!") {
            console.log('Cart saved successfully:', data.message);
        } else {
            console.error('Error saving cart:', data);  // Log the error if any
        }
    })
    .catch(error => {
        console.error('Error updating cart in session:', error);  // Log fetch errors
    });
}


// Function to update the cart display
function updateCart() {
    const cartItems = document.getElementById('cart-items');
    const totalPriceElement = document.getElementById('total-price');
    const cartItemCount = document.getElementById('cart-item-count');

    if (!cartItems || !totalPriceElement || !cartItemCount) return;

    cartItems.innerHTML = '';  // Clear existing cart items

    let total = 0;
    let totalItems = 0;

    cart.forEach((item, index) => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}">
            <span>${item.name} - Rs ${item.price}</span>
            <input type="number" value="${item.quantity}" min="1" id="quantity-${index}" class="quantity-input" onchange="updateItemQuantity(${index})">
            <button onclick="removeFromCart(${index})">Delete</button>
            <button class="btn4" data-index="${index}">Buy Now</button>  <!-- Buy Now button for individual products -->
        `;
        cartItems.appendChild(listItem);
        total += item.price * item.quantity;
        totalItems += item.quantity;

        // Debugging data-index
        console.log(`Index: ${index}, Data-index: ${item.name}`);
    });

    totalPriceElement.textContent = `Total: Rs ${total}`;
    cartItemCount.textContent = totalItems;

    // Show or hide the cart based on whether it has items
    document.getElementById('cart-section').style.display = cart.length > 0 ? 'block' : 'none';

    saveCartToSession(cart);  // Save the cart to the session
}

// Function to add an item to the cart
function addToCart(name, price, imageSrc) {
    const existingItemIndex = cart.findIndex(item => item.name === name);
    if (existingItemIndex !== -1) {
        cart[existingItemIndex].quantity += 1;  // Increment quantity if item already in cart
    } else {
        cart.push({ name, price, quantity: 1, image: imageSrc });  // Add new item to cart
    }

    updateCart();  // Update cart display
    saveCartToSession(cart);  // Save updated cart to session
}

// Function to remove an item from the cart
function removeFromCart(index) {
    cart.splice(index, 1);  // Remove the item from the cart
    updateCart();  // Update cart display
}

// Function to update the quantity of an item in the cart
function updateItemQuantity(index) {
    const quantityInput = document.getElementById(`quantity-${index}`);
    const newQuantity = parseInt(quantityInput.value);

    if (isNaN(newQuantity) || newQuantity < 1) {
        alert('Please enter a valid quantity.');
        quantityInput.value = 1;  // Reset to 1 if invalid quantity
        cart[index].quantity = 1;
    } else {
        cart[index].quantity = newQuantity;
    }

    updateCart();  // Recalculate and update the cart
}

// Function to toggle cart visibility
function toggleCart() {
    const cartSection = document.getElementById('cart-section');
    const currentDisplay = cartSection.style.display;

    if (currentDisplay === 'none' || currentDisplay === '') {
        cartSection.style.display = 'block';  // Show cart
    } else {
        cartSection.style.display = 'none';  // Hide cart
    }
}

document.body.addEventListener('click', function (event) {
    if (event.target && event.target.matches('.btn2')) {
        event.preventDefault();  // Prevent default link action

        const skinTxtDiv = event.target.closest('.skin-txt');
        const productText = skinTxtDiv ? skinTxtDiv.querySelector('p')?.textContent : '';

        if (productText) {
            const name = productText.split('only')[0]?.trim();
            const priceStr = productText.split('Rs')[1]?.trim();
            const price = priceStr ? parseFloat(priceStr) : NaN;  // Safely parse the price

            const imageSrc = event.target.closest('.skin-care').querySelector('img')?.src;

            // Ensure valid name, price, and imageSrc before calling addToCart
            if (name && !isNaN(price) && imageSrc) {
                addToCart(name, price, imageSrc);  // Add the product to the cart
            } else {
                console.error('Error extracting product details.');
            }
        } else {
            console.error('Product text not found.');
        }
    }
});


// Event listener for "Add to Cart" buttons
/*document.body.addEventListener('click', function (event) {
    if (event.target && event.target.matches('.btn2')) {
        event.preventDefault();  // Prevent default link action

        const productText = event.target.previousElementSibling.textContent;
        const name = productText.split('only')[0].trim();
        const price = parseFloat(productText.split('Rs')[1].trim());
        const imageSrc = event.target.closest('.skin-care').querySelector('img').src;

        addToCart(name, price, imageSrc);  // Add the product to the cart
    }
});*/

// Event listener for "Buy Now" button (for individual product)
document.body.addEventListener('click', function (event) {
    if (event.target && event.target.matches('.btn4')) {
        console.log('Buy Now button clicked!');
        event.preventDefault();  // Prevent default link action

        const index = event.target.getAttribute('data-index');
        console.log('Clicked index:', index);
        console.log('Cart array:', cart);  // Log the cart array to see its contents

        if (index === null || index === undefined || cart[index] === undefined) {
            console.error('Error: Invalid cart item index or item does not exist');
            return;
        }

        const item = cart[index];  // Get the product details at the specified index
        console.log('Item:', item);

        // Store product details in sessionStorage
        sessionStorage.setItem('productName', item.name);
        sessionStorage.setItem('productPrice', item.price);
        sessionStorage.setItem('productImage', item.image);
        sessionStorage.setItem('productQuantity', item.quantity);  // Save the quantity as well

        // Redirect to the checkout page
        window.location.href = '/checkout/';
    }
});

// Event listener for "Buy Now" button (for entire cart)
document.getElementById('buy-cart').addEventListener('click', function(event) {
    event.preventDefault();

    // Store the entire cart's details in sessionStorage
    sessionStorage.setItem('cart', JSON.stringify(cart));

    // Redirect to the checkout page
    window.location.href = '/checkout/';
});


/*// Initialize cart when the page loads
document.addEventListener('DOMContentLoaded', function () {
    loadCartFromSession();  // Load the cart from session on page load
});*/

// Cart Close Button: Close the cart section when clicked
const cartCloseBtn = document.getElementById('cart-close-btn');
if (cartCloseBtn) {
    cartCloseBtn.addEventListener('click', function () {
        document.getElementById('cart-section').style.display = 'none';  // Hide cart section
    });
}

// Clear Cart Button: Clear the cart when clicked
const clearCartBtn = document.getElementById('clear-cart');
if (clearCartBtn) {
    clearCartBtn.addEventListener('click', function () {
        cart = [];  // Clear the cart array
        updateCart();  // Update the cart display
    });
}

// Add this at the bottom of the script, ensuring it's executed after the page content is loaded
document.addEventListener('DOMContentLoaded', function () {
    loadCartFromSession();  // Load the cart from session on page load
});
// Optional: Ensure the cart section is displayed correctly after page load
/*document.addEventListener('DOMContentLoaded', function () {
    updateCart();  // Ensure the cart is updated after DOM is fully loaded
});*/
