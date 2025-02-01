from django.shortcuts import render
from .models import Booking, Menu
from .forms import BookingForm
from .serializers import MenuItemSerializer, BookingSerializer
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
import json
from datetime import datetime
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_class = [IsAuthenticated]
        if self.request.method != 'GET':
            permission_class.append(IsAdminUser)
        return [permission() for permission in permission_class]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_class = [IsAuthenticated]
        if self.request.method != 'GET':
            permission_class = [IsAdminUser]
        return [permission() for permission in permission_class]


class BookingView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            # admin could get all the bookings
            return Booking.objects.all()
        else:
            # customer can only get all the bookings that booking name is the customer's username
            return Booking.objects.filter(name=self.request.user.username)

    def get_permissions(self):
        return [IsAuthenticated()]


class SingleBookingView(generics.RetrieveDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # only admin could check/delete single bookings

    def get_permissions(self):
        return [IsAdminUser()]


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html', {"bookings": booking_json})


def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'book.html', context)

# Add your code here to create new views


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, 'menu_item.html', {"menu_item": menu_item})


@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist == False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')

    date = request.GET.get('date', datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')
