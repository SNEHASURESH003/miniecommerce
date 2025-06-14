from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, ProductForm
from .models import Product, Order
from django.contrib.auth.decorators import login_required

# Registration views
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password"
    return render(request, 'login.html', {'error': error})


from django.contrib.auth.decorators import login_required

# @login_required
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, 'admin_dashboard.html', {'products': products})

# @login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


# User dashboard
# @login_required
def dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def place_order(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        total_price = quantity * product.price
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        return render(request, 'order_summary.html', {'order': order})
    return redirect('dashboard')
