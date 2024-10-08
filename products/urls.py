
from django.urls import path
from. import views

urlpatterns = [
    
    path('',views.index,name='home'),
    path('productlist/',views.list_products,name='productlist'),
    path('<slug:category_slug>/',views.list_products,name='product_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',views.detail_product,name='product_detail'),
    path('search', views.product_search,name ='search')
   
]
