from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, ProductForm
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# ==== USER Registration ====
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # saves as normal user
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user_register.html', {'form': form})


# ==== ADMIN Registration ====
def admin_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # mark as admin
            user.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'admin_register.html', {'form': form})


# ==== Login (shared) ====
def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            error = "Invalid username or password"
    return render(request, 'login.html', {'error': error})


# ==== Logout ====
def user_logout(request):
    logout(request)
    return redirect('login')


# ==== Admin Dashboard ====
# @login_required
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, 'admin_dashboard.html', {'products': products})

# ==== Add Product ====
# @login_required


# ==== User Dashboard ====
# @login_required
def dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})


# ==== Product Detail ====
# @login_required
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})


# ==== Place Order ====
# @login_required
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
