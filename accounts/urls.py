
from django.urls import path
from. import views

urlpatterns = [
    
    path('register/',views.user_register,name='register'),
    path('signin/',views.user_login,name='signin'),
    path('logout/',views.user_logout,name='logout'),

]
