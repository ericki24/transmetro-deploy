"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .views import cerrar_sesion
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('guia/', include('guia.urls')),

    path('', include('dashboard.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('municipalidades/', include('municipios.urls')),
    path('lineas/', include('lineas.urls')),
    path('estaciones/', include('estaciones.urls')),
    path('accesos/', include('accesos.urls')),
    path('guardias/', include('guardias.urls')),
    path('parqueos/', include('parqueos.urls')),
    path('buses/', include('buses.urls')),
    path('pilotos/', include('pilotos.urls')),
    path('operadores/', include('operadores.urls')),
    path('alertas/', include('alertas.urls')),
    path('lineaestacion/', include('lineaestacion.urls')),
    path('buspiloto/', include('buspiloto.urls')),
    path('reportes/', include('reportes.urls')),
    path('mapa/', include('mapa.urls')),

    
]


# Errores personalizados
handler403 = 'django.views.defaults.permission_denied'
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'




if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
