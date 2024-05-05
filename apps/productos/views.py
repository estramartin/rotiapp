from django.shortcuts import render
from apps.productos.models import Producto
# Create your views here.


def main(request):
    template = 'public_html/index.html'
    productos = Producto.objects.all()
    context = {
        'productos': productos
    }
    return render(request, template, context)