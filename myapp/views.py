from django.shortcuts import render

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def blog(request):
    return render(request,"blog.html")

def menu(request):
    return render(request,"coffees.html")

def contact(request):
    return render(request,"contact.html")
