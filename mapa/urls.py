



from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_mapa, name='ver_mapa'),
    path('datos/', views.datos_mapa, name='datos_mapa'),
]



