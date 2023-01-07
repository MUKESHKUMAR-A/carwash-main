from django.db import models
import datetime
# Create your models here.
from django.contrib.auth.models import User
from django.utils.timezone import now
class Customer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.email

class Servicetype(models.Model):
    type_of_service = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.type_of_service)

class Service(models.Model):
    location = models.CharField(max_length=200, null=True, blank=True)
    service_type = models.ForeignKey(Servicetype, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.id)



class Booking(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Rejected', 'Rejected'),
    )
    customer_details = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    service_details = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateField(default=now)

    def __str__(self):
        return str(self.id)

class Tracker(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateField(default=now)
    count = models.IntegerField(default=0)
