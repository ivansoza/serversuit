"""
URL configuration for cion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static
from django_postalcodes_mexico import urls as django_postalcodes_mexico_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',include('cionapp.urls')),
    path('',include('generales.urls')),
    path('contribuyente/', include('contribuyente.urls')),
    path('personalizacion/', include('catalogos.urls')),
    path('agua/',include('agua.urls')),
    path('predio/',include('predio.urls')),
    path('ordenesPago/',include('ordenesPago.urls')),
    path('oficialiaPartes/',include('oficiliaPartes.urls')),
    path("op/",include('op.urls')),
    path('select2/', include('django_select2.urls')),
    path('postal-code/', include(django_postalcodes_mexico_urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)