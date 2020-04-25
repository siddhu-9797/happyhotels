from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from .serializers import BookingSerializer
from users.forms import CustomerSignUpForm, ManagerSignUpForm, CustomerSignInForm, RoomBookingForm
from users.models import User,Booking,Room, RoomAvailability, Manager, RoomAvailability
import datetime

now = timezone.now()

def ManagerSignUpView(request):
    if request.method=="POST":
        form = ManagerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, ('New user created. Login to get started'))
            return HttpResponse('<h1> Manager Successfully created</h1>')

    else:    
        form = ManagerSignUpForm()
    return render(request, 'signup.html', {'form': form})

def CustomerSignUpView(request):
    if request.method=="POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, ('New user created. Login to get started'))
            return HttpResponse('<h1> Customer Successfully created</h1>')

    else:    
        form = CustomerSignUpForm()
    return render(request, 'signup.html', {'form': form})

def CustomerSignInView(request):
    if request.method == "POST":
        form = CustomerSignInForm()
        username = request.POST['username']
        password = request.POST['password']
        print(username + " " + password)
        user = authenticate(username=username, password=password)
        print(user)
        print(user.has_perm('users.manager'))
        if user is not None:
            login(request, user)
            return HttpResponse("You've been logged in successfully")
    else:
        form = CustomerSignInForm()
    return render(request, 'signin.html', {'form':form})


# @login_required
# @permission_required('users.manager')
def Just_Checking(request):
    if request.user.is_authenticated and request.user.has_perm("users.manager"):
        return HttpResponse("Welcome authorised user!!")
    else:
        return HttpResponse("You don't have enough permission to access this page! :(")

@login_required
def bookRoom(request):
    if request.method == "POST":
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            date_time = form.cleaned_data['check_in']
            get_room = form.cleaned_data['room']
            get_room_advance_booking_date = get_room.inAdvance
            print(date_time - datetime.date.today())
            if((date_time - datetime.date.today()).days <= get_room_advance_booking_date):
                return HttpResponse((date_time - datetime.date.today()).days)
                
            else:
                return HttpResponse("Sorry please try again")

            # check_in_time = form.cleaned_data['check_in']
            # check_out_time = form.cleaned_data['check_out']
            # if(get_room.available_from > check_in_time or get_room.available_to < check_out_time ):
            #     return HttpResponse("Sorry your room cannot be booked")
            # if (form.cleaned_data['check_in'] <= form.cleaned_data['check_out']):
            # return HttpResponse(form.cleaned_data['check_in'].time())

            save_form = form.save(commit=False)
            print(save_form)
            print(request.user)
            print(type(request.user))
            save_form.customer = request.user
            save_form.save()
            

            print("hello")
            return HttpResponse("Room booked successfully")
    else:
        form = RoomBookingForm()
        
        return render(request, 'signup.html', {'form': form})

@login_required
def showBookings(request):
    get_bookings = Booking.objects.filter(customer = request.user)
    print(get_bookings)
    return render(request, 'showbookings.html', {'bookings':get_bookings})
@login_required
def deletebooking(request,id):
    get_booking = Booking.objects.filter(id = id)
    print(get_booking)
    get_booking.delete()
    # messages.success(request, 'Booking with ID ' + get_booking.id + ' is deleted successfully!')
    get_url = reverse('show_bookings')
    return HttpResponseRedirect(get_url)

def setRoom(request):
    if request.user.is_authenticated and request.user.has_perm("users.manager"):
        if request.method == 'POST':
            inAdvance = request.POST.get('inAdvance')
            new_room = Room()
            new_room.room_manager = Manager.objects.filter(room_manager = request.user).first()
            new_room.inAdvance = int(inAdvance)
            new_room.save()
            print(new_room.inAdvance)
            print(new_room.room_manager)
            return HttpResponse("Room created Successfully!")
        else:
            return render(request, 'setroom.html')
    else:
        return HttpResponse("You don't have enough permission to access this page! :(")

def showManagerRooms(request):
    if request.user.is_authenticated and request.user.has_perm("users.manager"):
        getManager = Manager.objects.filter(room_manager = request.user).first()
        getManagerRooms = Room.objects.filter(room_manager = getManager)
        if request.method == 'POST':
            pass
           

            
        else:
            return render(request, 'showManagerRooms.html', {'getManagerRooms':getManagerRooms})
    else:
        return HttpResponse("You don't have enough permission to access this page! :(")

def setAvailability(request, room_no):
    if request.user.is_authenticated and request.user.has_perm("users.manager"):
        getRoom = Room.objects.filter(room_no = room_no).first()
        # Get room's availabilities if any...
        getAvailabilitys = RoomAvailability.objects.filter(room = getRoom)
        print(getAvailabilitys)
        if request.method == 'POST':
            available_from = request.POST['check_in']
            available_to = request.POST['check_out']
            new_availability = RoomAvailability()
            new_availability.room = getRoom
            new_availability.available_from = available_from
            new_availability.available_to = available_to
            new_availability.save()
            return HttpResponse(str(new_availability.room.room_no) + new_availability.available_from + new_availability.available_to)
           

            
        else:
            return render(request, 'setavailability.html', {'getAvailabilitys':getAvailabilitys})
    else:
        return HttpResponse("You don't have enough permission to access this page! :(")


class Get_Booking_List(APIView):
    def get(self, request):
        bookings = Booking.objects.all()
        serialized_bookings = BookingSerializer(bookings, many=True)
        return Response(serialized_bookings.data)

def select_booking_date(request):
    if request.method == 'POST':
        get_date = request.POST['check_in_date']
        strp_date = datetime.datetime.strptime(get_date, "%Y-%m-%d").date()
        time_diff = (strp_date - datetime.date.today()).days
        filtered_rooms = Room.objects.filter(inAdvance__gte = time_diff)
        return render(request, 'showrooms.html', {'filtered_rooms':filtered_rooms, 'check_in_date':strp_date })
    else:
        return render(request, 'selectdate.html')

def selectslots(request, check_in_date, room_no):
    get_room = Room.objects.filter(room_no = room_no).first()
    get_room_availabilities = RoomAvailability.objects.filter(room = get_room)
    return render(request, 'selectslots.html', {'get_room_availabilities':get_room_availabilities, 'check_in_date':check_in_date, 'room_no':room_no })

    



