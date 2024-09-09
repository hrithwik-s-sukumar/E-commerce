from django.shortcuts import render,redirect
from.forms import RegistrationForm
from. models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def user_register(request):
    if request.method == 'POST':
       form = RegistrationForm(request.POST)
       if form.is_valid():
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           phone_number = form.cleaned_data['phone_number']
           email = form.cleaned_data['email']
           password = form.cleaned_data['password']
           username = email.split("@")[0]
           user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
           user.phone_number = phone_number
           user.save()
           messages.success(request,'Registration is successful')
           return render(request,'register.html')
    else:
        form = RegistrationForm()
    context = {
            'form': form
        }       
    return render(request,'register.html',context)

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        print(f"Trying to authenticate user: {email} with password: {password}")

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_admin:
                 return redirect('admindashboard')
            else: 
               auth.login(request, user)
               messages.success(request, 'You are now logged in')
               return redirect('home')
        else:
            print("Authentication failed")
            messages.error(request, 'Invalid credentials')
            return redirect('signin')

    return render(request, 'signin.html')


@login_required(login_url='home')
def user_logout(request):
    
    auth.logout(request)
    messages.success(request,'You are logged out')
    return redirect('home')


    


