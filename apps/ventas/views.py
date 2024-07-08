from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework. permissions import AllowAny 
from .models import Venta
# Create your views here.

class VentaQRViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        return render(request, 'ventas/qr.html')
    
    def retrieve(self, request, pk=None):
        venta = Venta.objects.get(pk=pk)
        qr_code = venta.qr_code
        return render(request, 'ventas/qr.html', {'qr_code': qr_code.url})
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        
        venta = Venta.objects.get(code=pk)
        print(venta)
        return Response({'status': 'ok'})