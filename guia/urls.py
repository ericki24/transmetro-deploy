from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_guia, name='ver_guia'),
    path('datos/', views.datos_guia, name='datos_guia'),
]
