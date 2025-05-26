from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_guardias, name='lista_guardias'),
    path('crear/', views.crear_guardia, name='crear_guardia'),
    path('editar/<int:pk>/', views.editar_guardia, name='editar_guardia'),
    path('eliminar/<int:pk>/', views.eliminar_guardia, name='eliminar_guardia'),
]
