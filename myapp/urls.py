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
    


]