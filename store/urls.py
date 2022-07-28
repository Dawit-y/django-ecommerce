from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('add_to_cart/<str:pk>/', views.add_to_cart, name='add-to-cart'),
    path('login/', views.login_form, name='login-form'),
    path('logout/', views.logout_form, name='logout-form'),    
    path('detail/<str:pk>/', views.view_product, name='detail'), 
    path('remove/<str:pk>/', views.remove, name="remove"),   
    path('register/', views.register, name="register")


]