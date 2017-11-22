from django.shortcuts import render
from hotel_app.models import City, Estate, Booking, Resident, RentalDate
from hotel_app.forms import ResidentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.utils.html import escape
import datetime
from datetime import timedelta
from pprint import pprint

# Create your views here.
def index(request):
    if request.method == 'GET':
        cities = City.objects.all()
        if 'filter' in request.GET:
            FilteredEstates = Estate.objects.all().filter(city = request.GET['idCity'], maxPax = request.GET['maxPax'])
            context = {
                'estates': FilteredEstates,
                'cities': cities
            }
            return render(request, 'estate/index.html', context)
        else:
            estates = Estate.objects.all()

            context = {
                'estates' : estates ,
                'cities' : cities
            }
            return render(request, 'estate/index.html', context)

def hosts(request):
    hosts = User.objects.all()
    context = {
        'hosts': hosts
    }
    return render(request, 'host/index.html', context)

def index_reserve(request, id_estate):
    if request.method == 'GET':
        #messages = None
        estate = Estate.objects.get(id = id_estate)
        print(estate.image)
        form = ResidentForm(initial={'name': 'Federico', 'surname': 'Palomero', 'email':'aldosivi@yahoo.com'})
        now = datetime.datetime.now
        context = {
            'e': estate,
            'form' : form,
            'now':now
        }
        return render(request, 'reserve/index.html', context)


    if request.method == 'POST': #Cuando se envía la info para la reserva
        estate = Estate.objects.get(id=id_estate)
        if(rentalDateIsAble(request.POST['dateFrom'], request.POST['dateTo'], estate)):
            resident = Resident(name=request.POST['name'], surname=request.POST['surname'], email=request.POST['email'])
            resident.save()
            booking = Booking(date=datetime.datetime.now(), total_price=estate.price, resident=resident)
            booking.save()
            saveRangeDate(srtToDate(request.POST['dateFrom']), srtToDate(request.POST['dateTo']), booking, estate)
            context = {
                'booking': booking,
                'e': estate
            }
            messages.success(request, 'Reserva concretada con éxito')
        else:
            messages.error(request, 'Rango de fechas no habilitado')
            context = {
                'e': estate
            }
        return render(request, 'reserve/index.html', context)

def saveRangeDate(dateFrom, dateTo, booking, estate):
    while(dateFrom <= dateTo):
        rentalDate = RentalDate.objects.create(date=dateFrom, booking=booking)
        rentalDate.estate.add(estate)
        rentalDate.save()
        dateFrom = dateFrom + timedelta(days=1)

def srtToDate(dateString):
    return datetime.datetime.strptime(dateString, "%Y-%m-%d").date()

def rentalDateIsAble(dateFrom, dateTo, estate):
    able = True
    rentalDates = RentalDate.objects.filter(date__range=[dateFrom, dateTo], booking__isnull=False ).count()
    if rentalDates != 0:
        able = False
    return able