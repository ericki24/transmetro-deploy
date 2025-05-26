from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_municipios, name='lista_municipios'),
    path('crear/', views.crear_municipio, name='crear_municipio'),
    path('editar/<int:pk>/', views.editar_municipio, name='editar_municipio'),
    path('eliminar/<int:pk>/', views.eliminar_municipio, name='eliminar_municipio'),
]
