from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Flight
from .forms import FlightForm
from django.db import models


def index(request):
    return render(request, 'flights/index.html')

def register_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_flights')
    else:
        form = FlightForm()
    return render(request, 'flights/register_flight.html', {'form': form})

def list_flights(request):
    flights = Flight.objects.all().order_by('price')
    return render(request, 'flights/list_flights.html', {'flights': flights})

def flight_statistics(request):
    total_national = Flight.objects.filter(type='Nacional').count()
    total_international = Flight.objects.filter(type='Internacional').count()
    avg_national_price = Flight.objects.filter(type='Nacional').aggregate(models.Avg('price'))['price__avg'] or 0

    context = {
        'total_national': total_national,
        'total_international': total_international,
        'avg_national_price': avg_national_price
    }
    return render(request, 'flights/statistics.html', context)