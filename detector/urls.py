from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    # Páginas principales
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('automaton/', views.automaton_explanation, name='automaton_explanation'),
    
    # Análisis de texto
    path('api/analyze/', views.api_analyze_text, name='api_analyze_text'),
    path('api/day-details/<str:date_str>/', views.api_day_details, name='api_day_details'),
    
    # Historial (requiere autenticación)
    path('history/', views.analysis_history, name='history'),
    path('detail/<int:analysis_id>/', views.analysis_detail, name='detail'),
]
