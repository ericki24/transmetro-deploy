from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_alertas, name='lista_alertas'),
    path('crear/', views.crear_alerta, name='crear_alerta'),
    path('editar/<int:pk>/', views.editar_alerta, name='editar_alerta'),
    path('eliminar/<int:pk>/', views.eliminar_alerta, name='eliminar_alerta'),
]
