from django.shortcuts import render,redirect
from products.models import Product
from .models import Cart, CartItem
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.



def _cart_id(request):

    cart = request.session.session_key
    if not cart:
        request.session.create()  # Ensure the session is created
        cart = request.session.session_key  # Retrieve the session key after creation
    return cart


def add_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    cart_id = _cart_id(request)  # Get or create session's cart_id

    # Use get_or_create to handle cart creation
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    # Try to find the cart item, or create it if it doesn't exist
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


def user_cart(request):

    cart_items = None
    total = 0
    quantity = 0
    cart_id = _cart_id(request)
    
    try:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax =(2*total)/100
        grand_total = total + tax

    except Cart.DoesNotExist:
        pass

    context = {
        'cart_items'  : cart_items,
        'total'       : total,
        'quantity'    : quantity,
        'tax'         : tax,
        'grand_total' : grand_total
    }

    return render(request, 'cart/cart.html', context)


def remove_cart(request, product_id):

    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()  # Update quantity if more than 1
        else:
            cart_item.delete()  # Remove cart item if quantity is 1
    except CartItem.DoesNotExist:
        pass  # Handle the case where the cart item does not exist

    return redirect('cart')  # Always redirect to the cart page after removal

def remove_cart_item(request,product_id):

    cart = Cart.objects.get(cart_id= _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product=product,cart= cart)
    cart_item.delete()
    return redirect('cart')


@login_required(login_url ='login')
def checkout_page(request):

    cart_items = None
    total = 0
    quantity = 0
    cart_id = _cart_id(request)
    
    try:
        cart = Cart.objects.get(cart_id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax =(2*total)/100
        grand_total = total + tax

    except Cart.DoesNotExist:
        pass

    context = {
        'cart_items'  : cart_items,
        'total'       : total,
        'quantity'    : quantity,
        'tax'         : tax,
        'grand_total' : grand_total
    }

    return render(request, 'cart/checkout.html', context)


