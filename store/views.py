from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Order, OrderItem
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def store(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']
    context = {'products' : products, 'cartItems' : cartItems}
    return render(request, 'store/store.html', context)
    
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
    return render(request, 'store/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}
        cartItems = order['get_cart_items']
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
    return render(request, 'store/checkout.html', context)
def updateItem(request):
    return JsonResponse('Item was added', safe=False)

@login_required(login_url='login-form')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product = product
       
    )
    order_qs = Order.objects.filter(customer=request.user, complete=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.orderitem_set.filter(product_id=product.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('store')
        else:
            order.orderitem_set.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('store')
    else:
        
        order = Order.objects.create(
            customer=request.user)
        order.orderitem_set.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('store')

def login_form(request):
    if request.user.is_authenticated:
        return redirect('store')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user doesnt exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'username or password is incorrect')
    return render(request, 'store/login-form.html', {})

def logout_form(request):
    logout(request)
    return redirect('store')
def view_product(request, pk):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    product = Product.objects.get(id=pk)
    return render(request, 'store/product-detail.html', {'product':product, 'cartItems' : cartItems})

def remove(request, pk):
    item = OrderItem.objects.get(id=pk)
   
    item.delete()
    return redirect('cart')

def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'store/register.html', {'form' : form})