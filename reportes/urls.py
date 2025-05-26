from django.urls import path
from . import views

urlpatterns = [
    path('', views.reporte_general, name='reporte_general'),
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
]
