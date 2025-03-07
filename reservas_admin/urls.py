from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_admin, name='home_admin'),
    path('signout/', views.signout_admin, name='signout_admin'),
    path('reserves/', views.reservas_admin, name='reservas_admin'),
    path('update_reserve/<int:reserve_id>/<str:status>/', views.update_reserve_status, name='update_reserve_status'),
]