from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Product, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('product_list')
    return render(request, 'shop/register.html', {'form': form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def place_order(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        quantity = int(request.POST['quantity'])
        total_price = product.price * quantity
        Order.objects.create(user=request.user, product=product, quantity=quantity, total_price=total_price)
        return render(request, 'shop/order_summary.html', {
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })
