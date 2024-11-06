from django.db import models


class Car(models.Model):
    registration_number = models.CharField(max_length=20, unique=True,primary_key=True)
    brand = models.CharField(max_length=50,null=True)  # Marque de la voiture
    model = models.CharField(max_length=50,null=True)  # Modèle de la voiture
    status = models.CharField(max_length=20, choices=[
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('under_review', 'Pris en charge'),
    ])

    def __str__(self):
        return f"{self.brand} {self.model} ({self.registration_number})"



