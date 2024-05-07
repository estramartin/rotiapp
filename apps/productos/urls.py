from django.urls import path
from .views import ViandaAutocomplete

urlpatterns = [
    path('vianda-autocomplete/', ViandaAutocomplete.as_view(), name='vianda-autocomplete'),
]