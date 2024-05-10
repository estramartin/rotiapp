from django.utils import timezone
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from rest_framework.viewsets import ViewSet 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.productos.models import Producto

from .serialzers import ProductoSerializer

class ViandaAutocomplete(AutocompleteJsonView):
    def get_queryset(self):        
        qs = super().get_queryset()        
        today = timezone.now().date()
        return qs.filter(agenda__fechas__fecha=today)
    

class ProductoViewSet(ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['activo']
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Producto.objects.all()

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        pass
    
    def retrieve(self, request, pk=None):
        pass
    
    def update(self, request, pk=None):
        pass
    
    def partial_update(self, request, pk=None):
        pass
    
    def destroy(self, request, pk=None):
        pass