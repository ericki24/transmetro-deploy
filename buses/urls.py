from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_buses, name='lista_buses'),
    path('crear/', views.crear_bus, name='crear_bus'),
    path('editar/<int:pk>/', views.editar_bus, name='editar_bus'),
    path('eliminar/<int:pk>/', views.eliminar_bus, name='eliminar_bus'),
]
