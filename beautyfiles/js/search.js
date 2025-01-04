// search.js

function searchProduct() {
    var searchQuery = document.getElementById('search-bar').value.toLowerCase().trim();

    // Redirect based on the query entered
    if (searchQuery === 'lipstick') {
        window.location.href = "{% url 'lipstick' %}";
    } else if (searchQuery === 'nailpolish') {
        window.location.href = "{% url 'nailpolish' %}";
    } else if (searchQuery === 'foundation') {
        window.location.href = "{% url 'foundation' %}";
    } else if (searchQuery === 'kajol') {
        window.location.href = "{% url 'kajol' %}";
    } else if (searchQuery === 'eyeshadow') {
        window.location.href = "{% url 'eyeshadow' %}";
    } else if (searchQuery === 'mascara') {
        window.location.href = "{% url 'kajol' %}";
    } else {
        // Handle case where no product matches
        alert('Product not found');
    }
}
