from django.urls import path
from . import views

app_name = 'monitoreo'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('municipios/', views.municipios_view, name='municipios'),
    path('api/ultimas/', views.api_ultimas, name='api_ultimas'),
    path('api/historial/<slug:slug>/<str:tipo>/', views.api_historial, name='api_historial'),
    path('exportar/<slug:slug>/', views.export_csv, name='export_csv'),
]