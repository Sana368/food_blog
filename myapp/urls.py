from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('blog/',views.blog,name='blog'),
    path('menu/',views.menu,name='menu'),
    path('contact/',views.contact,name='contact'),
    path('login1_view/',views.login1_view,name='login1_view'),
    path('signup/',views.signup,name='signup'),
    path('product/',views.food_product,name='food_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart_page/',views.cart_page,name='cart_page'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('order_summary/<int:order_id>/',views.order_summary,name='order_summary'),

    
    


]