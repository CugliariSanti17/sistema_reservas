from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reserve/', views.reservar_turno, name='reserve'),
    path('signup/', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('logout/', views.logOut, name='logout'),
    path('succesful_reserve/', views.succesful_reserve, name='succesful_reserve'),
    path('get_barbers/', views.get_barbers, name='get_barbers'),
    path('get_available_dates/', views.get_available_dates, name='get_available_dates'),
    path('get_available_times/', views.get_available_times, name='get_available_times'),
    path('booked_reserves/', views.booked_reserves, name='booked_reserves'),
]