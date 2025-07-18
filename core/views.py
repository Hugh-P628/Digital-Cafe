from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("core/index.html")
    products = [
        {"name": "Americano", "price": 110},
        {"name": "Cappuccino", "price": 140},
        {"name": "Espresso", "price": 100},  # ✅ Added Espresso
    ]
    context = {
        "product_data": products
    }
    return HttpResponse(template.render(context, request))
