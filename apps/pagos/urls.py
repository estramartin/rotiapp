from api.routers import APIRootRouter
from django.urls import path
from .views import Pago

router = APIRootRouter()
router.register('pagos', PagoViewSet, basename='pagos')