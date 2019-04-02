from django.urls import path
from . import views

urlpatterns = [
    path('', views.atd_ranking, name='atd_ranking'),
]