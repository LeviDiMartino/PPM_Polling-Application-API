from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Definiamo i ruoli fissi disponibili nel sistema
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('regular', 'Regular User'),
    )
    
    # Questo campo salverà il ruolo sul database (default: regular)
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='regular'
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

# Create your models here.
