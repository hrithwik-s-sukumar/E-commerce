from django.shortcuts import render,redirect
from.forms import RegistrationForm
from. models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
from carts.models import Cart,CartItem
import random
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            # Extracting cleaned data from form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Generate username from email
            username = email.split("@")[0]

            # Create a new user account
            request.session['user_data'] = {
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'email': email,
                'username': username,
                'password': password  
            }
        
            # Generate OTP and save it in session
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
            request.session['email'] = email

            # Send OTP email for verification
            send_mail(
                'Verify your email',
                f'Your OTP for verification is {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            # Notify user and render OTP verification page
            messages.success(request, "OTP has been sent to your email for verification.")
            return render(request, 'verify.html')

        else:
            # If form is invalid, display error message
            messages.error(request, "Something went wrong. Please check your inputs.")

    else:
        # If the request method is not POST, show an empty registration form
        form = RegistrationForm()

    # Context to render the registration page
    context = {
        'form': form
    }

    return render(request, 'register.html', context)


def verify_otp(request):
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp') 
        stored_otp = request.session.get('otp')  
        stored_email = request.session.get('email')

        if str(stored_otp) == entered_otp:
            user = Account.objects.get(email=stored_email)
            user.is_active = True 
            user.save()

            del request.session['otp']
            del request.session['email']

            messages.success(request, "OTP verified successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        print(f"Trying to authenticate user: {email} with password: {password}")

        # Authenticate the user
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            # Check if the user is an admin
            if user.is_admin:
                return redirect('admindashboard')

            try:
                print('entering inside try block')
                # Retrieve the cart using a custom cart ID (assuming _cart_id function exists)
                cart = Cart.objects.get(cart_id=_cart_id(request))
                
                # Check if any cart items exist in the cart
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                
                if is_cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    print('cart_item')

                    # Assign each cart item to the authenticated user
                    for item in cart_items:
                        item.user = user  
                        item.save()

            except Cart.DoesNotExist:
                print('entering inside except block')
                # If no cart exists, pass silently or handle the error accordingly
                pass

            # Log in the user and redirect to the home page
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')

        else:
            # Authentication failed
            print("Authentication failed")
            messages.error(request, 'Invalid credentials')
            return redirect('signin')

    # If request method is GET, render the login form
    return render(request, 'signin.html')


@login_required(login_url='home')
def user_logout(request):
    
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('home')


    


