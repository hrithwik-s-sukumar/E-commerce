from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect,reverse
from. models import Product
import random
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.db.models import Q



# Create your views here.
def index(request):

    products = Product.objects.all().filter(is_available = True) 
    context = {
        'products': products,  
    }
    return render(request,'home.html',context)
    

def list_products(request,category_slug = None):

    categories = None
    products   = None
    product_count =0
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available = True)
        paginator = Paginator(products,1)
        page  = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products,4)
        page  = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count' : product_count,
    }
    return render(request,'productslist.html',context)




def detail_product(request,category_slug,product_slug):

    try:
        single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product = single_product)
        
    except Exception as e:
        raise e

    context = {
      'single_product' : single_product,
      'in_cart'        : in_cart,
    }

    return render(request, 'productdetails.html',context )



def product_search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if 'keyword':
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            # product_count =product.count()

    context = {
      'products' : products,
    #   'product_count' :product_count,
     
    }       

    return render(request, 'productlist.html' )


    