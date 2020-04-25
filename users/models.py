from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    class Meta:
        permissions = [
            ("manager", "I'm a manager"),
        ]
 

class Manager(models.Model):
    room_manager = models.OneToOneField(User, on_delete = models.CASCADE)
    employee_id = models.IntegerField()
    

class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete = models.CASCADE)
    phone_no = models.IntegerField()
    


class Room(models.Model):
    room_no = models.AutoField(primary_key=True)    
    room_manager = models.ForeignKey(Manager, on_delete = models.CASCADE)
    inAdvance = models.IntegerField()
    isAvailable = models.BooleanField(default=True)
    

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete = models.CASCADE) 
    customer = models.ForeignKey(User, on_delete = models.CASCADE)
    check_in_date = models.DateField( blank=False, null=False)
    check_out_date = models.DateField( blank=False, null=False)
    no_of_people = models.IntegerField()
    price = models.IntegerField(default = 0)

class RoomAvailability(models.Model):
    room = models.ForeignKey(Room, on_delete = models.CASCADE) 
    available_from =  models.TimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    available_to =  models.TimeField(auto_now=False, auto_now_add=False, blank=False, null=False)


