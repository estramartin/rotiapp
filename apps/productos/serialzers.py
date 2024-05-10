from rest_framework import serializers

from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ['precio_venta', 'precio_costo']
        extra_kwargs = {
            'precio_venta': {'read_only': True},
            'precio_costo': {'read_only': True}
        }