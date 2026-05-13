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
    

class AppVersion(models.Model):
    version = models.CharField(max_length=20, help_text="Ex: 1.0.1")
    apk_file = models.FileField(upload_to='apks/updates/', blank=True, null=True, help_text="Le fichier APK de l'application (optionnel si URL externe fournie)")
    external_url = models.URLField(blank=True, null=True, help_text="URL externe vers le fichier APK (Cloud, etc.)")
    release_notes = models.TextField(blank=True, null=True, help_text="Les nouveautés de cette mise à jour")
    force_update = models.BooleanField(default=False, help_text="Cocher pour obliger l'utilisateur à mettre à jour")
    is_active = models.BooleanField(default=True, help_text="Est-ce la version actuellement déployée ?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Version de l'application"
        verbose_name_plural = "Versions de l'application"

    def __str__(self):
        return f"Version {self.version}"

    def save(self, *args, **kwargs):
        # Si on active cette version, on désactive toutes les autres pour n'avoir qu'une seule version active
        if self.is_active:
            AppVersion.objects.filter(is_active=True).update(is_active=False)
        super(AppVersion, self).save(*args, **kwargs)



