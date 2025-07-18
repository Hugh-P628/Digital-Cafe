from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import (
    login, logout, authenticate
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product

# Existing views


def login_view(request):
    if request.method == 'GET':
        template = loader.get_template("core/login_view.html")
        return HttpResponse(template.render({}, request))
    elif request.method == 'POST':
        submitted_username = request.POST['username']
        submitted_password = request.POST['password']
        user_object = authenticate(
            username=submitted_username, password=submitted_password)

        if user_object is None:
            messages.add_message(request, messages.INFO, 'Invalid login.')
            return redirect(request.path_info)

        login(request, user_object)
        return redirect('index')


@login_required
def index(request):
    template = loader.get_template("core/index.html")
    products = Product.objects.all()
    context = {
        "user": request.user,
        "product_data": products,
    }
    return HttpResponse(template.render(context, request))


@login_required
def product_detail(request, product_id):
    template = loader.get_template("core/product_detail.html")
    p = Product.objects.get(id=product_id)
    context = {
        "product": p
    }
    return HttpResponse(template.render(context, request))

# ✅ Add this function
