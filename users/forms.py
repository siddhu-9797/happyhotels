import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from users.models import Manager, Customer, Booking, Room, RoomAvailability
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerSignUpForm(UserCreationForm):
    phone_no = forms.IntegerField() 
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name','last_name' ,'username', 'email', 'password1', 'password2']
    
    @transaction.atomic   
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        new_customer = Customer.objects.create(customer=user, phone_no = self.cleaned_data.get('phone_no'))
    
class ManagerSignUpForm(UserCreationForm):
    employee_id = forms.IntegerField() 
    class Meta(UserCreationForm):
        model = User
        fields = ['first_name','last_name' ,'username','employee_id', 'email', 'password1', 'password2']
    
    @transaction.atomic   
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        user.save()
        new_manager = Manager.objects.create(room_manager=user, employee_id = self.cleaned_data.get('employee_id'))
        
        permission = Permission.objects.get(codename='manager')
        print(permission)
        print(user.user_permissions.add(permission))

class CustomerSignInForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class ManagerSignInForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class RoomBookingForm(forms.ModelForm):
    # check_in = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget())
    # check_out = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget())
    
    check_in = forms.DateField()
    check_out = forms.DateField()
    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out', 'no_of_people']
    
    
    
    @transaction.atomic
    def save(self, commit=True):
        bookRoom = super().save(commit=False)
        # checkIn = self.cleaned_data['check_in_time']
        # checkOut = self.cleaned_data['check_out_time']
        # Checkin = datetime.datetime.strptime(checkIn, "%Y-%m-%d").date()
        # Checkout = datetime.datetime.strptime(checkOut, "%Y-%m-%d").date()
        print( self.cleaned_data['check_in'])
        bookRoom.check_in_time = self.cleaned_data['check_in']
        bookRoom.check_out_time = self.cleaned_data['check_out']
        bookRoom.price = 1000
        return bookRoom 
        
# class RoomBookingForm(forms.ModelForm):
#     class Meta:
#         model = Room
#         fields = ['inAdvance']
        






            