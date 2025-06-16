from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='registration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('events/', views.events, name='events'),
    path('pay_levy/<int:levy_id>/', views.pay_levy, name='pay_levy'),
    path('committees/<int:committee_id>/', views.committee_detail, name='committee_detail'),
]