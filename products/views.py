from django.shortcuts import render,get_object_or_404
from. models import Product,Category
import random
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator





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

    if category_slug != None:

        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available = True)
        product_count = product_count()
        

    else:

        products = Product.objects.all().filter(is_available = True)
        paginator = Paginator(products,3)
        page  = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count' : product_count,

    }

    return render(request,'productslist.html',context)

def detail_product(request, id):

    product = get_object_or_404(Product, id=id)
    user_id = request.session.get('user_id')  # Retrieve user_id from session
    print(f"User ID in product_detail view: {user_id}")  # Debugging line
    
    context = {
        'product': product,
        'user_id': user_id
    }

    return render(request, 'productdetails.html', context)