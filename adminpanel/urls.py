# urls.py
from django.urls import path
from . import views

urlpatterns = [
 
    path('admindashboard/', views.admin_dashboard, name='admindashboard'),
    path('userdashboard/', views.user_dashboard, name='userdashboard'),
    path('productdashboard/', views.product_dashboard, name='productdashboard'),
    path('categorydashboard/', views.category_dashboard, name='categorydashboard'),
    path('adduser/', views.user_add, name='adduser'),
    path('edituser/<int:user_id>/', views.user_edit, name='edituser'),
    path('blockuser/<int:user_id>/', views.user_block, name='blockuser'),
    path('addproduct/', views.product_add, name='addproduct'),
    path('editproduct/<int:id>/', views.product_edit, name='editproduct'),
    path('deleteproduct/<int:id>/', views.product_delete, name='deleteproduct'),
    path('addcategory/', views.category_add, name='addcategory'),

]

