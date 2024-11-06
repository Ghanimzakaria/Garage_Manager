from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('client', 'Client')
    ]
    role = models.CharField(max_length=20, choices=USER_ROLES)
    def __str__(self):
        return f"{self.role}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname}"
#dsvfqsv
#QSC

class Car(models.Model):
    registration_number = models.CharField(max_length=20, unique=True,primary_key=True)
    brand = models.CharField(max_length=50,null=True)  # Marque de la voiture
    model = models.CharField(max_length=50,null=True)  # Modèle de la voiture
    status = models.CharField(max_length=20, choices=[
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('under_review', 'Pris en charge'),
    ])
    assigned_emplyee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return f"{self.brand} {self.model} ({self.registration_number})"



