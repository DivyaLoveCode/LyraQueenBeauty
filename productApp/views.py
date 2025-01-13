
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib import messages
from .models import LoginUser, Enquiry, Order
from django.http import JsonResponse
from decimal import Decimal

import json


# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# Create your views here.
def search(request):
    search_query = request.GET.get('query', '').lower().strip()

    if search_query == 'lipstick':
        return redirect('lipstick')
    elif search_query == 'nailpolish':
        return redirect('nailpolish')
    elif search_query == 'foundation':
        return redirect('foundation')
    elif search_query == 'kajol':
        return redirect('kajol')
    elif search_query == 'eyeshadow':
        return redirect('eyeshadow')
    elif search_query == 'mascara':
        return redirect('mascara')
    else:
        return HttpResponseBadRequest('Product not found')  # Or handle 404


def home(request):
    return render(request, 'home.html')

def index(request):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session
    user = None
    if user_id:
        user = LoginUser.objects.get(id=user_id)# Retrieve the user object from the database
        # Clear any leftover cart data from the session
    request.session.pop('cart', None)  # Ensure cart is empty on index page load
    request.session.pop('cart_item_count', None)  # Reset cart item count
    return render(request, 'index.html', {'user': user})

'''def index(request):
    return render(request, 'index.html')'''


def about(request):
    return render(request, 'about us.html')


def contact(request):
    return render(request, 'contact.html')


def lipstick(request):
    return render(request, 'lipstick.html')


def nailpolish(request):
    return render(request, 'nailpolish.html')


def kajol(request):
    return render(request, 'kajol.html')


def foundation(request):
    return render(request, 'foundation.html')


def eyeshadow(request):
    return render(request, 'eye shadow.html')


'''def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup .html')

        if LoginUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'signup .html')

        user = LoginUser(first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully!')
        return redirect('login')

    return render(request, 'signup .html')'''

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Check if the passwords match
        if password != password_confirm:
            return JsonResponse({
                'status': 'error',
                'message': 'Passwords do not match'
            })

        # Check if the email already exists
        if LoginUser.objects.filter(email=email).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Email already exists'
            })

        # Create and save the new user
        user = LoginUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password  # Hash the password before saving
        )
        user.save()

        # Return success response with rendered login page HTML
        return JsonResponse({
            'status': 'success',
            'message': 'Registration successful! Please log in.',
            'redirect_url': '{% url "login" %}'  # Include the URL for the login page
        })

    # If the request is not POST, just render the registration page (for normal page load)
    return render(request, 'signup .html')


def login_view(request):
    messages.get_messages(request).used = True

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Attempt to fetch the user by email using filter (no exception handling)
        user = LoginUser.objects.filter(email=email).first()
        # `first()` will return the first match or None


        if user and user.password == password:  # If user exists and the password matches
            # Store the user ID in session to track the logged-in user
            request.session['user_id'] = user.id
           # messages.success(request, f'Welcome, {user.first_name}!')
            return redirect('index')  # Redirect to the index page after successful login
        else:
            messages.error(request, 'Invalid email or password')  # Error message for incorrect login

    return render(request, 'log form.html')


def logout_view(request):
    # Clear the session (log out the user)
    request.session.flush()  # This will remove the user from the session
   # messages.info(request, 'You have successfully logged out.')
    # Clear messages explicitly by marking them as 'used'
    messages.get_messages(request).used = True
    # Redirect to the homepage after logout
    return redirect('home')  # Redirect to the homepage where login/register buttons are
'''def logout_view(request):
    # Clear the session (log out the user)
    request.session.flush()  # This will remove the user from the session
    messages.info(request, 'You have successfully logged out.')
    return redirect('home')  # Redirect to the homepage after logout'''

'''def login(request):
    if request.method == "POST": 
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = LoginUser.objects.filter(email=email, password=password)
        if user.exists():
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'log form.html')'''



def enquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Create a new Enquiry object and save it
        enq = Enquiry(name=name, email=email, subject=subject, message=message)
        enq.save()

        # Add a success message
        messages.success(request, 'Your form has been submitted successfully!')

        # Redirect to the contact page
        return redirect('contact')
    return render(request, 'contact.html')


def get_cart(request):
    # Check if 'cart' is present in the session
    cart_data = request.session.get('cart', None)  # This returns None if 'cart' doesn't exist in the session

    # Print the cart data for debugging
    print("Cart data from session:", cart_data)  # This will print to the server logs

    if cart_data is None:
        print("No cart found in session, initializing an empty cart.")
        cart_data = []  # Initialize as empty array if cart doesn't exist

    # Send cart data back to the client
    return JsonResponse({'cart': cart_data})


def save_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_data = data.get('cart', [])

            if not isinstance(cart_data, list):
                return JsonResponse({'error': 'Cart data must be an array.'}, status=400)

            # Save cart data to session
            request.session['cart'] = cart_data
            request.session.modified = True
            return JsonResponse({'message': 'Cart saved successfully!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# Function to save the cart in the session
'''@csrf_exempt
def save_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['cart'] = data['cart']
        return JsonResponse({'status': 'success'})'''

def checkout(request):
    cart_data = request.session.get('cart', [])

    if not cart_data:
        return redirect('index')  # Redirect to index if the cart is empty

    # Calculate total price
    total_price = sum(item['price'] * item['quantity'] for item in cart_data)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')

        if not name or not email or not phone or not address or not zipcode:
            return render(request, 'checkout.html', {'cart_data': cart_data, 'total_price': total_price, 'error_message': 'Please fill in all the fields.'})

        # Create the order in the database
        order = Order.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            zipcode=zipcode,
            total_price=total_price,
        )

        # Store order ID and cart data temporarily in session
        request.session['order_id'] = order.id
        request.session['cart_data'] = cart_data

        # Redirect to payment gateway page
        return redirect('payment-gateway', order_id=order.id)

    return render(request, 'checkout.html', {'cart_data': cart_data, 'total_price': total_price})




def order_success(request, order_id):
    # Try to fetch the order by order_id
    try:
        # Retrieve the order from the database
        order = Order.objects.get(id=order_id)

        # Get cart data stored in session (the cart data was stored during checkout)
        cart_data = request.session.get('cart_data', [])

        # Print cart data to the console to debug
        print(cart_data)  # This will print the cart data to the Django server console

        # Optionally clear session data after the order is successfully placed
        request.session.pop('order_id', None)
        request.session.pop('cart_data', None)

        # Clear the cart item count from session (if you're tracking it)
        request.session.pop('cart_item_count', None)

        # Render the order success template with the order and cart data
        return render(request, 'order_success.html', {'order': order, 'cart_data': cart_data})

    except Order.DoesNotExist:
        # Handle the case where the order does not exist in the database
        return redirect('index')  # Redirect to home page if order does not exist


def payment_gateway(request, order_id):
    # Retrieve the order by ID
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('index')  # Redirect to home page if the order doesn't exist

    # Convert the total price (Decimal) to integer (paise)
    amount = int(order.total_price * 100)  # Razorpay expects the amount in paise (1 INR = 100 paise)

    # Razorpay currency
    currency = 'INR'

    # Create an order with Razorpay
    try:
        razorpay_order = client.order.create(dict(
            amount=amount,
            currency=currency,
            payment_capture='1'  # '1' indicates that the payment will be automatically captured
        ))
    except razorpay.errors.RazorpayError as e:
        # Handle Razorpay API error
        print(f"Error creating Razorpay order: {e}")
        return redirect('index')  # Redirect if Razorpay order creation fails

    # Save the Razorpay order ID to your order in the database
    order.razorpay_order_id = razorpay_order['id']
    order.save()

    # Pass the order details to the template for payment
    context = {
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    }

    return render(request, 'payment_gateway.html', context)

def payment_success(request, order_id):
    # Get payment details from the form
    payment_id = request.POST.get('razorpay_payment_id')
    order_id_from_razorpay = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')

    # Verify the payment signature
    params = {
        'razorpay_order_id': order_id_from_razorpay,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    # Verify the payment signature with Razorpay
    try:
        client.utility.verify_payment_signature(params)

        # If signature is valid, mark the order as paid
        order = Order.objects.get(id=order_id)
        order.status = 'paid'
        order.payment_status = 'completed'
        order.razorpay_payment_id = payment_id
        order.save()

        # Clear cart data from session after successful payment
        request.session.pop('cart', None)  # Remove cart data from session
        request.session.pop('cart_item_count', None)  # Reset cart item count

        # Redirect to an order success page or show a success message
        return render(request, 'order_success.html', {'order': order})

    except razorpay.errors.SignatureVerificationError:
        # If signature verification fails, handle the error
        return JsonResponse({'error': 'Payment verification failed'}, status=400)
'''def payment_gateway(request, order_id):
    # Retrieve the order by ID
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('index')  # Redirect to home page if the order doesn't exist

    # Handle POST request when the user selects a payment method
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        # Update the payment method in the order
        order.payment_method = payment_method
        order.save()

        # Redirect to the payment success page after payment selection
        return redirect('payment-success', order_id=order.id)

    # Render payment gateway page
    return render(request, 'payment_gateway.html', {'order': order})

def payment_success(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect('index')  # Redirect to home page if the order doesn't exist

    # Simulate successful payment (this could be replaced with actual payment verification logic)
    order.status = 'paid'  # Mark the order as paid
    order.payment_status = 'completed'  # Mark payment as completed
    order.save()

    # Clear the cart or session after successful payment (optional)
    request.session['cart'] = []  # Clear the cart

    # Redirect to an order success page (for example)
    return redirect('order-success', order_id=order.id)'''


