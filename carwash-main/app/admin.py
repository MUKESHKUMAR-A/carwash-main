from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Service)
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Servicetype)
admin.site.register(Tracker)