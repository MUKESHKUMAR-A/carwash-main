from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .decorators import unauthenticated_user
import datetime
# Create your views here.
def error_404_view(request, exception):
    data = {}
    return render(request, 'error_404.html', data)
    
@unauthenticated_user
def welcomePage(request):
    context = {}
    return render(request,'welcome.html',context)

@unauthenticated_user
def register(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmpassword')
            
            if password == confirmpassword:
                user = User.objects.create_user(username,email,password)
                customer = Customer.objects.create(user=user, username=username, email=email, password=password)
                customer.save()

                return redirect('login')
            else:
                messages.info(request, 'password not matching')
    except:
        messages.info(request, 'some details are already taken by other user')
    context = {}
    return render(request, 'register.html', context)

@login_required(login_url='login')
def homePage(request):
    context = {}
    return render(request, 'homepage.html', context)

@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Username or password incorrect')

    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('welcome')

@login_required(login_url='login')
def showServices(request):
    if request.method == 'POST':
        location = request.POST.get('place')
        services = Service.objects.all().filter(location=location)
        context = {'services':services}
        return render(request, 'showservices.html',context)


@login_required(login_url='login')
def bookService(request,pk):
    sample_user = request.user
    email = sample_user.email
    customer = Customer.objects.get(email=email)
    service = Service.objects.get(id=pk)
    try:
        track = Tracker.objects.get(customer=customer, date_created=datetime.date.today())
        track.count += 1
        if track.count > 5:
            messages.info(request, 'bookings limit exceeded for today for customer')
            return redirect('home')
        booking = Booking.objects.create(
            customer_details = customer,
            service_details = service,
            status = 'Pending',
        )
        track.save()
        booking.save()
        return redirect('home')
    except:
        track = Tracker.objects.create(customer=customer, date_created=datetime.date.today())
        track.count += 1
        track.save()
        booking = Booking.objects.create(
            customer_details = customer,
            service_details = service,
            status = 'Pending',
        )
        booking.save()
        return redirect('home')

@login_required(login_url='login')
def showBookings(request):
    sample_user = request.user
    email = sample_user.email
    customer = Customer.objects.get(email=email)
    bookings = customer.booking_set.all()
    context = {'bookings':bookings}
    return render(request, 'bookings.html',context)


@login_required(login_url='login')
def adminAddPlaces(request):
    if request.user.is_staff:
        if request.method == 'POST':
            location = request.POST.get('place')
            service = request.POST.get('service')
            try:
                s = Servicetype.objects.get(type_of_service=service)
            except:
                s = Servicetype.objects.create(type_of_service=service)
                s.save()
            new_service = Service.objects.create(location=location, service_type=s)
            new_service.save()
            return redirect('home')
        context = {}
        return render(request, 'adminaddplace.html', context)
    else:
        messages.info(request, 'You are not admin')
        context = {}
        return render(request, 'homepage.html', context)

@login_required(login_url='login')
def adminShowAllBookings(request):
    if request.user.is_staff:
        bookings = Booking.objects.all()
        context = {'bookings': bookings}
        return render(request, 'adminviewbookings.html', context)
    else:
        messages.info(request, 'You are not admin')
        context = {}
        return render(request, 'homepage.html', context)


@login_required(login_url='login')
def adminModifyStatus(request,pk,status):
    if request.user.is_staff:
        booking = Booking.objects.get(id=pk)
        if status == '1':
            booking.status = 'Accepted'
        else:
            booking.status = 'Rejected'
        booking.save()
        return redirect('home')
    else:
        messages.info(request, 'You are not admin')
        context = {}
        return render(request, 'homepage.html', context)

