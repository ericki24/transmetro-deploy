from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_estaciones, name='lista_estaciones'),
    path('crear/', views.crear_estacion, name='crear_estacion'),
    path('editar/<int:pk>/', views.editar_estacion, name='editar_estacion'),
    path('eliminar/<int:pk>/', views.eliminar_estacion, name='eliminar_estacion'),
]
