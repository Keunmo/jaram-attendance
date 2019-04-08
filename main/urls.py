from django.urls import path
from . import views

urlpatterns = [
    path('', views.atd_ranking, name='atd_ranking'),
    path('ranking/', views.full_ranking, name='full_ranking'),
    path('chulseokcheck/', views.atd_check, name='atd_check_page')
]