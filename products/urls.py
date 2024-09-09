
from django.urls import path
from. import views

urlpatterns = [
    path('',views.index,name='home'),
    path('productlist/',views.list_products,name='productlist'),
    path('productdetail/<int:id>/', views.detail_product, name='productdetail'),
    
]
