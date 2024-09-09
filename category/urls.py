from django.urls import path
from. import views

urlpatterns = [

    path('categorylist/',views.list_category,name='categorylist'),
]



