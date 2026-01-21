# assistant/urls.py
from django.urls import path
from . import views

app_name = 'assistant'

urlpatterns = [
    # Main assistant dashboard
    path('', views.assistant_dashboard, name='dashboard'),
    
    # API endpoints
    path('api/chat/', views.assistant_chat, name='chat'),
    path('api/analysis/', views.generate_analysis, name='analysis'),
    path('api/query/', views.natural_language_query, name='nl_query'),
]
