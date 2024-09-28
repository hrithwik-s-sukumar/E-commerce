from django.shortcuts import render, redirect
from carts.models import Cart, CartItem
from .forms import OrderForm
import datetime
from .models import Order

# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items   = CartItem.objects.filter(user=current_user)
    if not cart_items.exists():

        print("No items found for the current user in the cart.")
    cart_count   = cart_items.count()
    print("Cart count:", cart_count)
    print("Cart items:", cart_items) 
    if cart_count <= 0:
        return redirect('productlist')  # Redirect if no items in cart

    grand_total = 0
    tax = 0

    # Calculate total and quantity
    for cart_item in cart_items:
        total    += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name  = form.cleaned_data['last_name']
            data.email      = form.cleaned_data['email']
            data.phone      = form.cleaned_data['phone']
            data.address_1  = form.cleaned_data['address_1']
            data.address_2  = form.cleaned_data['address_2']
            data.city       = form.cleaned_data['city']
            data.state      = form.cleaned_data['state']
            data.country    = form.cleaned_data['country']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax        = tax
            data.ip         = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d  = datetime.date(yr, mt, dt)

            current_date = d.strftime("%Y%d%m")
            order_number = current_date + str(data.id)  # Corrected to use 'data.id'
            data.order_number = order_number
            data.save()

            # After successful save, redirect to a confirmation page or similar
            return redirect('order_confirmation', order_number=order_number)

    return render(request, 'cart/placeorder.html', {'form': form, 'cart_items': cart_items, 'grand_total': grand_total})



    