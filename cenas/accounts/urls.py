from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.logear, name="accounts-login"),
    path('authenticate/', views.autenticar, name="accounts-authenticate"),
    path('logout/', views.cerrarsesion, name="accounts-logout"),
    path('panel/', views.panel, name="accounts-panel")
]
