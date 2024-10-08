from django.shortcuts import render,redirect
from.forms import RegistrationForm
from. models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from carts.views import _cart_id
from carts.models import Cart,CartItem


# Create your views here.
def user_register(request):
    if request.method == 'POST':
       form = RegistrationForm(request.POST)
       if form.is_valid():
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           phone_number = form.cleaned_data['phone_number']
           email = form.cleaned_data['email']
           password = form.cleaned_data['password']
           username = email.split("@")[0]
           user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
           user.phone_number = phone_number
           user.save()
           messages.success(request,'Registration is successful')
           return render(request,'register.html')
    else:
        form = RegistrationForm()
    context = {
            'form': form
        }       
    return render(request,'register.html',context)

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


    


