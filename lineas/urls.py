from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_lineas, name='lista_lineas'),
    path('crear/', views.crear_linea, name='crear_linea'),
    path('editar/<int:pk>/', views.editar_linea, name='editar_linea'),
    path('eliminar/<int:pk>/', views.eliminar_linea, name='eliminar_linea'),
]
