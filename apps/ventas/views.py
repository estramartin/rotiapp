import requests
import logging

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework. permissions import AllowAny
from .models import Venta
# Create your views here.

logger = logging.getLogger(__name__)

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
    
    @action(detail=False, methods=['GET'])
    def location(self, request):
        ip_address = get_client_ip_address(request)
        print(ip_address)
        geolocation_data = get_geolocation(ip_address)
        return Response(geolocation_data)

from ipware import get_client_ip

def get_client_ip_address(request):
    print(request.META)
    client_ip, is_routable = get_client_ip(request)
    logger.info(f"client_ip {client_ip}, is_routable {is_routable}")
    if client_ip is None:
        return None
    if is_routable:
        return client_ip
    else:
        return None

def get_geolocation(ip_address):
        print(ip_address)
        response = requests.get(f'https://geolocation-db.com/json/{ip_address}&position=true')
        return response.json()
