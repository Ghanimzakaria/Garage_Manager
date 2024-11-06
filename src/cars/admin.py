from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Client, Employee, Car

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Car)

