from django.contrib import admin
from users.models import Manager, Customer, Room, Booking, User, RoomAvailability

# Register your models here.

admin.site.register(Manager)
admin.site.register(Customer)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(User)
admin.site.register(RoomAvailability)

