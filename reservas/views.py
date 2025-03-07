from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReserveForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Barber, Reserve
from datetime import datetime, timedelta
from django.utils.timezone import now
# Create your views here.

CustomUser = get_user_model()
@login_required
def reservar_turno(request):
    if request.method == 'GET':
        form = ReserveForm()
        return render(request, 'reservar_turno.html', {
            'form': form,
        })
    elif request.method == 'POST':           
        form = ReserveForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False) # No guarda en la BD aún
            reserva.user = request.user #Asigna el usuario actual
            reserva.save() # Ahora sí guarda en la BD
            
            return JsonResponse({
                'to_email': reserva.email,
                'client_name': reserva.client,
                'barber': reserva.barber.name,
                'price': str(reserva.barber.price),
                'date': reserva.date.strftime('%Y-%m-%d'),
                "time": reserva.time.strftime('%H:%M'),
            })
            
        
        return render (request, 'reservar_turno.html', {
            'form': form,
            'error': 'Error al reservar turno'
        })
        
def home(request):
    return render(request, 'home.html')

def signUp(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup.html', {
            'form': form
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('reserve')
            except IntegrityError: #Cuando un usuario se repite
                return render(request, 'signup.html', {
                    'form': UserCreationForm(), 
                    'error': 'El nombre de usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'error': 'Las contraseñas no coinciden'
        })
            
def signIn(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'signin.html', {
            'form': form
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if user.role == 'barbero':
                return redirect('home_admin')
            else:
                return redirect('reserve')
        else:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Nombre de usuario o contraseña incorrectos'
            })

@login_required
def logOut(request):
    logout(request)
    return redirect('home')

@login_required
def succesful_reserve(request):
    return render(request, 'succesful_reserve.html')

def get_barbers(request):
    barbers = Barber.objects.all().values('id', 'name', 'hability', 'price')
    return JsonResponse(request, {'barbers': barbers})

def get_available_dates(request):
    barber_id = request.GET.get('barber_id')
    
    if barber_id:
        try:
            barber = Barber.objects.get(id=barber_id)
            barber_data = {
                'name': barber.name,
                'price': barber.price,
            }
            
            #generar los proximos 7 dias disponibles:
            available_dates = []
            for i in range (7):
                day = now().date() + timedelta(days=i)
                
                #Verificamos si hay horarios disponibles para ese dia:
                booked_times = list(Reserve.objects.filter(barber=barber, date=day).values_list('time', flat=True))
                
                if any(time not in booked_times for time in range(barber.start_time.hour, barber.end_time.hour)):
                    available_dates.append(day.strftime("%Y-%m-%d"))
            
            return JsonResponse({'dates': available_dates, 'barber': barber_data})
        
        except Barber.DoesNotExist:
            return JsonResponse({'error': 'Barbero no encontrado'}, status=404)
        
    return JsonResponse({'error': 'Invalid request'}, status=404)

def get_available_times(request):
    barber_id = request.GET.get('barber_id')
    date_selected = request.GET.get('date')
    
    if barber_id and date_selected:
        try:
            barber = Barber.objects.get(id=barber_id)
            booked_times = list(Reserve.objects.filter(barber=barber, date=date_selected).values_list('time', flat=True))
            
            available_times  = []
            current_time = barber.start_time
            
            while current_time < barber.end_time:
                if current_time not in booked_times:
                    available_times.append(current_time.strftime('%H:%M'))
                
                current_time = (datetime.combine(now().date(), current_time) + timedelta(minutes=30)).time()
            
            return JsonResponse({'times': available_times})
        except Barber.DoesNotExist:
            return JsonResponse({'error': 'Barbero no encontrado'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=404)


def booked_reserves(request):
    reserves = Reserve.objects.filter(user = request.user).order_by('-date', '-time')
    return render(request, 'booked_reserves.html', {
        'reserves': reserves
    })
