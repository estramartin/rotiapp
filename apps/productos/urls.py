

from django.urls import path
from . import views


urlpatterns = [
    path('main/', views.main, name='main'),
    #path('localidad/codigo_postal/search/', views.search_localidad_codigo_postal, name='localidad_codigo_postal_search'),
    #path('municipio/search/', views.search_municipio, name='municipio_search'),
]