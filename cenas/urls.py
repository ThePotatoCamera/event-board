from django.urls import path, include
from django.urls.conf import re_path
    
from . import views

app_name = 'cenas'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^cenas/', views.redirectcenas, name='redirectcenas'),
    path('<int:evento_id>/', views.detail, name='detail'),
    path('<int:pk>/recuento/', views.ResultsView.as_view(), name='recuento'),
    path('<int:evento_id>/seleccionar/', views.seleccionar, name='seleccionar'),
    path('eventos-selecciones/', views.seleccion_evento_obtener, name='eventos-selecciones'),
    path('obtener-selecciones/<int:evento_id>/', views.obtener_selecciones, name='obtener-selecciones')
]

# Importaciones de URL

urlpatterns += [
    re_path(r'^accounts/', include('cenas.accounts.urls'), name='accounts')
]
