from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_operadores, name='lista_operadores'),
    path('crear/', views.crear_operador, name='crear_operador'),
    path('editar/<int:pk>/', views.editar_operador, name='editar_operador'),
    path('eliminar/<int:pk>/', views.eliminar_operador, name='eliminar_operador'),
]
