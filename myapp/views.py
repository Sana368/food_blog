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
            return redirect('food_product')
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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login1_view')  # Redirects to 'user_login' if the user is not logged in
def food_product(request):
    return render(request, 'product.html')

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

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CartItem  # Assuming CartItem model exists for the user's cart
 # If you have a form for billing details
from django.http import Http404

# def checkout(request):
#     # Get the cart items of the logged-in user
#     cart_items = CartItem.objects.filter(user=request.user)
    
#     # if not cart_items:
#     #     # If no items in the cart, redirect to the cart page
#     #     messages.error(request, "Your cart is empty.")
#     #     return redirect('cart_page')

#     # Calculate total price for the cart items
#     total_price = sum(item.get_total_price() for item in cart_items)
    
#     if request.method == 'POST':
#         # Handle form submission
#         full_name = request.POST.get('full_name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')

#         if not full_name or not email or not phone or not address:
#             messages.error(request, "Please fill in all the billing details.")
#             return redirect('checkout')
        

#           order = Order.objects.create(
#             user=request.user,
#             total_price=total_price,
#             full_name=full_name,
#             email=email,
#             phone=phone,
#             address=address
#         )
        
#         # Save each cart item as an order item
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 price=item.product.price
#             )
#             item.delete()  # Clear cart after order placement
        
#         messages.success(request, "Checkout successful. Proceed to payment.")

#         # Redirect to a payment gateway or confirmation page
#         return redirect('order_summary', order_id=order.id)  # Adjusted redirect with order_id
    
#     return render(request, 'checkout.html', {
#         'cart_items': cart_items,
#         'total_price': total_price
#     })




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CartItem, Product
from django.http import Http404

# Add item to cart
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

    if not created:
        cart_item.quantity += 1  # Increment quantity if product already in cart
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart_page')
@login_required(login_url='login1_view')
# View the cart page
def cart_page(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        # Update cart item quantity
        if 'quantity' in request.POST:
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity'))
            


            try:
                cart_item = CartItem.objects.get(id=item_id, user=request.user)

                # Update the quantity if valid
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                    messages.success(request, f"Quantity for {cart_item.product.name} updated to {quantity}.")
                else:
                    messages.error(request, "Quantity must be greater than 0.")
            except CartItem.DoesNotExist:
                raise Http404("Cart item not found.")
            return redirect('cart_page')

        # Remove cart item
        elif 'remove' in request.POST:
            item_id = request.POST.get('item_id')

            try:
                cart_item = CartItem.objects.get(id=item_id, user=request.user)
                cart_item.delete()
                messages.success(request, f"{cart_item.product.name} has been removed from your cart.")
            except CartItem.DoesNotExist:
                raise Http404("Cart item not found.")
            return redirect('cart_page')

    return render(request, 'cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

# Remove item from cart
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, f"{cart_item.product.name} has been removed from your cart.")
    except CartItem.DoesNotExist:
        raise Http404("Cart item not found.")

    return redirect('cart_page')



from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from .models import CartItem

def update_cart(request, item_id):
    """
    Function to update the quantity of a cart item.
    """
    if request.method == 'POST':
        # Get the new quantity from the POST request
        new_quantity = int(request.POST.get('quantity'))
        
        try:
            # Get the cart item for the given item_id and user
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            
            if new_quantity > 0:
                # Update the quantity of the cart item
                cart_item.quantity = new_quantity
                cart_item.save()
                # Display a success message
                messages.success(request, f"Quantity for {cart_item.product.name} updated to {new_quantity}.")
            else:
                # Show an error if the quantity is less than 1
                messages.error(request, "Quantity must be greater than 0.")
        
        except CartItem.DoesNotExist:
            # If the cart item is not found
            raise Http404("Cart item not found.")
        
        # Redirect to the cart page after updating
        return redirect('cart_page')
    
    # If the request method is not POST, redirect back to the cart page
    return redirect('cart_page')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import  CartItem, Order, OrderItem

def checkout(request):
    # Get the cart items of the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)
    
    # if not cart_items:
    #     # If no items in the cart, redirect to the cart page
    #     messages.error(request, "Your cart is empty.")
    #     return redirect('cart_page')

    # Calculate total price for the cart items
    total_price = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        # Handle form submission
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if not full_name or not email or not phone or not address:
            messages.error(request, "Please fill in all the billing details.")
            return redirect('checkout')
        
        # Save the order details
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address
        )
        
        # Save each cart item as an order item
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.delete()  # Clear cart after order placement
        
        messages.success(request, "Checkout successful. Proceed to payment.")

        # Redirect to a payment gateway or confirmation page
        return redirect('order_summary', order_id=order.id)  # Adjusted redirect with order_id
    
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def order_summary(request, order_id):
    order = Order.objects.filter(id=order_id, user=request.user).first()
    if not order:
        messages.error(request, 'Order not found.')
        return redirect('cart')
    order_items = OrderItem.objects.filter(order=order)
    
    total_quantity = sum(item.quantity for item in order_items)
    total_price = sum(item.quantity * item.price for item in order_items)
    
    order_items_with_names = [
        {
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.price,
            'total': item.quantity * item.product.price
        }
        for item in order_items
    ]
    
    return render(request, 'order_summary.html', {
        'order': order,
        'order_items': order_items, 
        'total_quantity': total_quantity, 
        'total_price': total_price
    })



from django.conf import settings

from django.http import JsonResponse
from .models import Order

import razorpay
from django.conf import settings

client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

from django.shortcuts import redirect

def razorpay_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        total_amount = order.total_price  # Assuming you have a field 'total_price' in your Order model
        # Create a Razorpay payment object here and return the response
        # After successful payment, redirect to the receipt URL
        return redirect('receipt',order_id=order_id)
    return JsonResponse({'error': 'Invalid Request'})




from django.shortcuts import render
from django.shortcuts import render

def receipt(request):
    # Retrieve the latest order from the database (assuming the latest order is the one to display)
    latest_order = Order.objects.latest('id')

    context = {'order': latest_order}
    return render(request, 'receipt.html', context)


from django.shortcuts import render
from .models import Order  # Import your Order model (adjust the import according to your project structure)

@login_required
def receipt_history(request):
    orders = Order.objects.filter(user=request.user).order_by('order_date')

    return render(request, 'receipt_history.html', {
        'orders': orders
    })


def user_logout(request):
    logout(request)
    return redirect('login1_view')
    