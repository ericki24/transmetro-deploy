from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_parqueos, name='lista_parqueos'),
    path('crear/', views.crear_parqueo, name='crear_parqueo'),
    path('editar/<int:pk>/', views.editar_parqueo, name='editar_parqueo'),
    path('eliminar/<int:pk>/', views.eliminar_parqueo, name='eliminar_parqueo'),
]
