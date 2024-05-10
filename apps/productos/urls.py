from django.urls import path
from api.routers import APIRootRouter
from .views import (
    ViandaAutocomplete,
    ProductoViewSet
    )


router = APIRootRouter()
router.register('productos', ProductoViewSet, basename='productos')

urlpatterns = [
    path('vianda-autocomplete/', ViandaAutocomplete.as_view(), name='vianda-autocomplete'),
]