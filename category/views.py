from django.shortcuts import render

# Create your views here.

def list_category(request):
    return render(request,'categorylist.html')

