from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import IntegrityError
from reservas.models import Reserve


# Create your views here.
def is_barber(user):
    return user.role == 'barbero'

@user_passes_test(is_barber)
def home_admin(request):
    return render(request, 'home_admin.html') 
            

@login_required
def signout_admin(request):
    logout(request)
    return redirect('home')
@login_required
def reservas_admin(request):
    reservas = Reserve.objects.all()
    return render(request, 'reservas_admin.html', {
        'reservas': reservas
    })
    
def update_reserve_status(request, reserve_id, status):
    reserve = get_object_or_404(Reserve, pk=reserve_id)
    
    if status in ['atendida', 'cancelada']:
        reserve.status = status
        reserve.save()
    
    return redirect('reservas_admin')