from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('main/', views.atd_ranking, name='atd_ranking'),
    path('ranking/', views.full_ranking, name='full_ranking'),
    path('chulseokcheck/', views.atd_check, name='atd_check_page'),
    path('register/', views.register, name='register_page'),
    path('register_popup_rbp/', views.register_with_qrcode, name='register_qrcode'),
    path('welcome/', views.welcome_message, name='welcome_page'),
]