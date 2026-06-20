import secrets
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class VerificationCode(models.Model):
    PURPOSE_CHOICES = [
        ('REGISTER', 'Inscription'),
        ('PASSWORD_RESET', 'Réinitialisation de mot de passe'),
    ]

    identifier = models.CharField(max_length=150, help_text="Téléphone ou Email")
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['identifier', 'purpose', 'is_used']),
            models.Index(fields=['code']),
        ]

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    @staticmethod
    def generate_code():
        return ''.join(secrets.choice('0123456789') for _ in range(6))

    def __str__(self):
        return f"{self.purpose} - {self.identifier} - {self.code}"


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
        from django.db import transaction
        if self.is_active:
            with transaction.atomic():
                AppVersion.objects.select_for_update().filter(is_active=True).update(is_active=False)
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)



