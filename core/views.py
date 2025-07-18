from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Product, CartItem, Transaction, LineItem


def login_view(request):
    if request.method == 'GET':
        return render(request, "core/login_view.html")
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.add_message(request, messages.INFO, 'Invalid login.')
            return redirect(request.path_info)
        login(request, user)
        return redirect('index')


@login_required
def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {
        "user": request.user,
        "product_data": products
    })


@login_required
def product_detail(request, product_id):
    if request.method == 'GET':
        product = Product.objects.get(id=product_id)
        return render(request, 'core/product_detail.html', {"product": product})
    elif request.method == 'POST':
        qty = int(request.POST['quantity'])
        product = Product.objects.get(id=request.POST['product_id'])
        CartItem.objects.create(
            user=request.user, product=product, quantity=qty)
        messages.add_message(request, messages.INFO,
                             f'Added {qty} of {product.name} to your cart')
        return redirect('index')


@login_required
def checkout(request):
    if request.method == 'GET':
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, 'core/checkout.html', {'cart_items': cart_items})
    elif request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        transaction = Transaction.objects.create(
            user=request.user, created_at=timezone.now())
        for item in cart_items:
            LineItem.objects.create(
                transaction=transaction, product=item.product, quantity=item.quantity)
            item.delete()
        messages.add_message(request, messages.INFO,
                             'Thank you for your purchase!')
        return redirect('index')


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # Add totals to each transaction object
    for transaction in transactions:
        total = sum(
            item.product.price * item.quantity
            for item in transaction.lineitem_set.all()
        )
        transaction.total_amount = total  # ✅ attach total dynamically

    return render(request, 'core/transaction_history.html', {
        'transactions': transactions,
    })
