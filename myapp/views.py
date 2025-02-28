from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ContactMessage



def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def blog(request):
    return render(request,"blog.html")

def menu(request):
    return render(request,"coffees.html")


def contact(request):
        if request.method == "POST":
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone_number = request.POST.get('phone_number', '')
            message = request.POST.get('message', '')
            if name and email and phone_number and message:
                ContactMessage.objects.create(name=name, email=email, phone_number=phone_number, message=message)
                messages.success(request, "Your message has been sent successfully!")
                return redirect('contact')
            else:
                messages.error(request, "Please fill in all fields.")
    
    # Render the contact form
        return render(request, 'contact.html')

    

def login1_view(request):
    if request.method =='POST':
        username =request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'invalid username or password')


    return render(request,"login.html")

def signup(request):
    if request.method =='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'email already exists')
            else:
                 user = User.objects.create_user(username=username, email=email, password=password)
                 user.save()
                 messages.success(request, 'Account created successfully! Please login.')
                 return redirect('login1_view')
        else:
         messages.error(request, 'Passwords do not match')

    return render(request,"signup.html")

