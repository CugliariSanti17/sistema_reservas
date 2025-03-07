from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('barbero', 'Barbero'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cliente')
    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Barber(models.Model):
    name = models.CharField(max_length=100)
    hability = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=5, decimal_places=3, default=0.000)
    
    def __str__(self):
        return f'{self.name} - {self.hability} - ${self.price}'
    
class Reserve (models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
    ]
    
    client = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField()
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendiente')
    
    class Meta:
        unique_together = ('barber', 'date', 'time') # Evitar duplicacion de reservas
    def __str__(self):
        return f'{self.client} reserve w/ {self.barber} - on {self.date} - {self.time} ({self.status})'
    