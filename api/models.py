from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class RendezVous(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('CANCELLED', 'Annulé'),
    ]

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date_rdv = models.DateField(null=True, blank=True, help_text="Date souhaitée pour le rendez-vous")
    message = models.TextField(null=True, blank=True, help_text="Message ou motif du rendez-vous")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RDV: {self.user.username} - {self.date_rdv}"
    



