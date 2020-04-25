"""happyhotels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from users.views import (
    ManagerSignUpView, CustomerSignUpView, CustomerSignInView, 
    Just_Checking, bookRoom, showBookings, deletebooking, setRoom, 
    showManagerRooms, setAvailability, Get_Booking_List,select_booking_date, selectslots
        )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manager_signup/', ManagerSignUpView, name = 'manager_signup'),
    path('customer_signup/', CustomerSignUpView, name = 'customer_signup'),
    path('customer_signin/', CustomerSignInView, name = 'customer_signin'),
    path('check/', Just_Checking, name = 'just_checking'),
    path('book/', bookRoom, name = 'book_room'),
    path('showbookings/', showBookings, name = 'show_bookings'),
    path('setroom/', setRoom, name = 'setroom'),
    path('selectdate/', select_booking_date, name = 'selectdate'),
    url(r'^showbookings/cancel/(?P<id>[0-9]+)$', deletebooking, name='deletebooking'),
    url(r'^setavailability/(?P<room_no>[0-9]+)$', setAvailability, name='setavailability'),
    path('managerooms/', showManagerRooms, name = 'managerooms'),
    url(r'^bookingapi$', Get_Booking_List.as_view()),
    url(r'^selectslots/(?P<check_in_date>(\d{4}-\d{2}-\d{2}))/(?P<room_no>[0-9]+)/$', selectslots, name='selectslots'),

]
