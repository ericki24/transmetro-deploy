from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_accesos, name='lista_accesos'),
    path('crear/', views.crear_acceso, name='crear_acceso'),
    path('editar/<int:pk>/', views.editar_acceso, name='editar_acceso'),
    path('eliminar/<int:pk>/', views.eliminar_acceso, name='eliminar_acceso'),
]
