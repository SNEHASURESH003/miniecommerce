from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProductForm
from .models import Product, Order

# === USER REGISTRATION ===
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user_register.html', {'form': form})


# === ADMIN REGISTRATION (only superusers) ===
@login_required
def admin_register(request):
    # Ensure only superusers can access this page
    if not request.user.is_superuser:
        return redirect('login')  # Redirect others to user login

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Mark as admin
            user.save()
            return redirect('admin_login')  # ✅ Redirect to admin login page
    else:
        form = UserRegisterForm()

    return render(request, 'admin_register.html', {'form': form})

# === USER LOGIN ===
def user_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)
        if user and not user.is_staff:
            login(request, user)
            return redirect('dashboard')  # ✅ This is the redirect after login
        error = "You are not authorized as a user."
    return render(request, 'login.html', {'error': error})



# === ADMIN LOGIN ===
def admin_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        error = "Superuser credentials required."
    return render(request, 'admin_login.html', {'error': error})


# === LOGOUT ===
def user_logout(request):
    logout(request)
    return redirect('login')


# === ADMIN DASHBOARD (superuser only) ===
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    products = Product.objects.all()
    return render(request, 'admin_dashboard.html', {'products': products})


# === ADD PRODUCT (superuser only) ===
@login_required
def add_product(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


# === USER DASHBOARD ===
@login_required
def dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})


# === PRODUCT DETAIL ===
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


# === PLACE ORDER ===
@login_required
def place_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
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
