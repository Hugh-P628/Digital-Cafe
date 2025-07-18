from django.http import HttpResponse
from django.template import loader
from .models import Product

def index(request):
    template = loader.get_template("core/index.html")
    products = Product.objects.all()
    context = {"product_data": products}
    return HttpResponse(template.render(context, request))

def product_detail(request, product_id):
    template = loader.get_template("core/product_detail.html")
    p = Product.objects.get(id=product_id)
    context = {"product": p}
    return HttpResponse(template.render(context, request))
