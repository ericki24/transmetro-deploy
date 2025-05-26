from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_lineaestacion, name='lista_lineaestacion'),
    path('crear/', views.crear_lineaestacion, name='crear_lineaestacion'),
    path('editar/<int:pk>/', views.editar_lineaestacion, name='editar_lineaestacion'),
    path('eliminar/<int:pk>/', views.eliminar_lineaestacion, name='eliminar_lineaestacion'),
]
