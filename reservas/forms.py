from django import forms
from .models import Reserve, Barber

class ReserveForm(forms.ModelForm):
    
    barber = forms.ModelChoiceField(
        queryset=Barber.objects.all(),  # Obtiene los barberos disponibles
        widget=forms.Select(attrs={
            'class': 'form-control-custom border-warning text-light bg-dark', 
            'style': 'border-radius: 5px; padding: 10px;',
            'id': 'id_barber',
            'name': 'barber',
            })
    )
    
    date = forms.CharField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control-custom border-warning text-light bg-dark', 
            'style': 'border-radius: 5px; padding: 10px;',
            'id': 'id_date',
            'name': 'date',
            })
    )
    
    time = forms.CharField(
        required=False,
        widget = forms.Select(attrs={
            'class': 'form-control-custom border-warning text-light bg-dark', 
            'style': 'border-radius: 5px; padding: 10px;',
            'id': 'id_time',
            'name': 'time',
            })
    )

    class Meta:
        model = Reserve
        fields = ['client', 'email', 'phone', 'barber', 'date', 'time']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control-custom form-select border-warning text-light bg-dark', 'placeholder': 'Nombre y Apellido', 'style': 'border-radius: 5px; padding: 10px;', 'name': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control-custom form-select border-warning text-light bg-dark', 'placeholder': 'Correo electrónico', 'style': 'border-radius: 5px; padding: 10px;', 'name': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control-custom form-select border-warning text-light bg-dark', 'placeholder': 'Número de teléfono', 'style': 'border-radius: 5px; padding: 10px;', 'name': 'phone'}),
        }
