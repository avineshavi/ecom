# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SellerRegistrationForm, ProductForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import Product, Seller, Cart

def login_user(request):
    
    if request.user.username == 'guest_user':
        logout(request)
    if request.user.is_authenticated and request.user.username != 'guest_user':
        products = Product.objects.all()
        return render(request, 'products/list_products.html', {'products': products})
        # return redirect('list_products')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                products = Product.objects.all()
                return render(request, 'products/list_products.html', {'products': products})
                # return redirect('list_products')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('custom_login') 


def register_seller(request):
    
    if request.user.username == 'guest_user':
        logout(request)
    
    if request.user.is_authenticated and request.user.username != 'guest_user':
        return redirect('list_products')
    
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            seller = Seller(user=user)
            seller.save()
            login(request, user)
            return redirect('list_products')
    else:
        form = SellerRegistrationForm()
    return render(request, 'registration/register_seller.html', {'form': form})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if (request.user):
                product.seller = request.user.seller
                product.save()
                return redirect('list_products')
            else:
                
                return redirect('register_seller')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})


@login_required
def list_products(request):
    if hasattr(request.user, 'seller'):
        products = Product.objects.filter(seller=request.user.seller)
    else:
        products = Product.objects.all()
    return render(request, 'products/list_products.html', {'products': products})


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


@login_required
def view_cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    products_in_cart = user_cart.products.all()
    return render(request, 'products/view_cart.html', {'products_in_cart': products_in_cart})

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        user_cart.products.add(product)
    else:
        # For guest users, use a unique identifier for the guest_user_id
        guest_user_id = request.session.get('guest_user_id')
        guest_cart, created = Cart.objects.get_or_create(guest_user_id=guest_user_id)
        guest_cart.products.add(product)
    return redirect('view_cart')


def login_as_guest(request):
    guest_username = 'guest_user'
    guest_user, created = User.objects.get_or_create(username=guest_username)
    login(request, guest_user)
    request.session['guest_user_id'] = guest_username
    return redirect('list_products')


def custom_404(request, exception=None):
    return render(request, 'registration/404.html', status=404)