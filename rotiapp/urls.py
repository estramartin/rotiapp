"""
URL configuration for Rotiapp users project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from api.routers import api_urls

ADMIN_SITE_HEADER = getattr(settings, 'ADMIN_SITE_HEADER', 'Rotiapp admin')
ADMIN_SITE_TITLE = getattr(settings, 'ADMIN_SITE_TITLE', 'Rotiapp admin')

admin.site.site_header = ADMIN_SITE_HEADER
admin.site.site_title = ADMIN_SITE_TITLE

schema_view = get_schema_view(
    openapi.Info(
        title="RestoNauta - APIDOCS",
        default_version='v1',
        description="Documentación",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="estramartin@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

handler500 = 'rest_framework.exceptions.server_error'
handler400 = 'rest_framework.exceptions.bad_request'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls'))
]

auth_urls = [
   path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),
]


urlpatterns += [
    path('auth/', include(auth_urls)),
    path('api/v1/', include(api_urls())),
]


# if settings.DEBUG:   
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # only works on debug!

