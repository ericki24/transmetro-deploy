from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pilotos, name='lista_pilotos'),
    path('crear/', views.crear_piloto, name='crear_piloto'),
    path('editar/<int:pk>/', views.editar_piloto, name='editar_piloto'),
    path('eliminar/<int:pk>/', views.eliminar_piloto, name='eliminar_piloto'),
]
