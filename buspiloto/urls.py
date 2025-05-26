from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_buspiloto, name='lista_buspiloto'),
    path('crear/', views.crear_buspiloto, name='crear_buspiloto'),
    path('editar/<int:pk>/', views.editar_buspiloto, name='editar_buspiloto'),
    path('eliminar/<int:pk>/', views.eliminar_buspiloto, name='eliminar_buspiloto'),
]
