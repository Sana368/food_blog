from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ContactMessage
from .models import  Product



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

def food_product(request):
    return render(request,'product.html')

# def food(request):
#     return render(request,'food.html')


# def food1(request):
#     return render(request,'food1.html')

# def food2(request):
#     return render(request,'food2.html')
from .models import Product 
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})




from django.shortcuts import render, redirect
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required

@login_required
def cart_page(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    # Get all the items in the cart
    cart_items = cart.cart_items.all()

    return render(request, 'cart_page.html', {'cart': cart, 'cart_items': cart_items})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    # Get the product by its ID
    product = get_object_or_404(Product, id=product_id)

    # Get the user's cart (create a new one if it doesn't exist)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # If the product is already in the cart, increase the quantity by 1
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_page')  # Redirect to the cart page after adding the item



from django.shortcuts import render

def checkout(request):
    # Your logic for the checkout view
    return render(request, 'checkout.html')





