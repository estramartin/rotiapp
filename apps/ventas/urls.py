from api.routers import APIRootRouter
from django.urls import path
from .views import VentaQRViewSet

router = APIRootRouter()
router.register('ventaqr', VentaQRViewSet, basename='ventaqr')



