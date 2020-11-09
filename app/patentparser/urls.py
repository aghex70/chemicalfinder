"""chemfinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

TITLE = "Chemfinder API"

admin.site.site_header = 'Chemical finder API'
admin.site.index_title = 'Chemical finder API'

SchemaView = get_schema_view(
    info=openapi.Info(
        title="chemfinder API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="aghex70@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    validators=["ssv", "flex"],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chemfinder.urls')),
    url(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


