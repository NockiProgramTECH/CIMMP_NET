import re
import urllib.parse
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class VideoMixin:
    """Mixin pour extraire l'ID de vidéo et générer l'URL d'embed de manière sécurisée."""
    
    def extract_video_id(self):
        if not self.url:
            return None
        
        url = self.url.strip()
        
        # YouTube Patterns: standard, be, embed, shorts, live
        youtube_regex = r'(?:v=|\/|embed\/|shorts\/|live\/|youtu\.be\/|^)([\w-]{11})(?:[\?&]|$)'
        
        if 'youtube' in url or 'youtu.be' in url:
            match = re.search(youtube_regex, url)
            return match.group(1) if match else None
        
        # Facebook doesn't always have a clear ID in the URL, 
        # but their embed plugin works best with the full URL.
        return None

    def get_embed_url(self):
        if not self.url:
            return ""
        
        url = self.url.strip()
        
        # YouTube
        if 'youtube' in url or 'youtu.be' in url:
            video_id = self.extract_video_id()
            if video_id:
                return f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0"
        
        # Facebook
        if 'facebook.com' in url or 'fb.watch' in url:
            producer_match = re.search(r'live\/producer\/(\d+)', url)
            if producer_match:
                video_id = producer_match.group(1)
                url = f"https://www.facebook.com/video.php?v={video_id}"

            encoded_url = urllib.parse.quote(url, safe='')
            return f"https://www.facebook.com/plugins/video.php?href={encoded_url}&show_text=0&adapt_container_width=true&height=315&appId"

        # Vimeo
        if 'vimeo.com' in url:
            match = re.search(r'vimeo\.com\/(\d+)', url)
            if match:
                return f"https://player.vimeo.com/video/{match.group(1)}"

        # Bonus: TikTok
        if 'tiktok.com' in url:
            match = re.search(r'video\/(\d+)', url)
            if match:
                return f"https://www.tiktok.com/embed/v2/{match.group(1)}"

        return ""

class Predication(models.Model, VideoMixin):
    # Informations principales
    img_couverture=models.ImageField(upload_to ='predications/')
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField()
    url_video =models.URLField(blank=True, help_text="URL de la vidéo YouTube ou Facebook")
    video_file = models.FileField(
        upload_to='videos/', blank=True, null=True,
        validators=[FileExtensionValidator(['mp4', 'webm', 'ogg', 'mov', 'avi'])]
    )

    @property
    def url(self):
        if self.video_file:
            # Si on a un fichier uploadé, on utilise le storage configuré
            return self.video_file
        return self.url_video # Sinon on garde l'ancienne méthode (YouTube/FB)
    audio =models.FileField(upload_to="audio",blank=True,null=True)
    resume = models.TextField(blank=True)
    verset_principal = models.CharField(max_length=100, blank=True)
    contenu = models.TextField(blank=True)

    predicateur = models.CharField("Preacher", max_length=200)
    interprete = models.CharField("Interprete", max_length=200, null=True, blank=True)
    theme = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Predication"
        verbose_name_plural = "Predications"
        ordering = ['date']
    
    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)[:50]
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('predication_detail', args=[str(self.slug)])

class Evenement(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateTimeField()
    lieu = models.CharField(max_length=25, default="Eglise CIMPP")
    image = models.ImageField(upload_to='evenements/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evenement"
        verbose_name_plural = "Evenements"
        ordering = ['name']
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('evenement_detail', args=[str(self.slug)])

class Temoignages(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    subjet =models.CharField(max_length=50)
    temoignage =models.TextField()
    created_at  =models.DateTimeField(auto_created=True,default=timezone.now)
    published =models.BooleanField(default=False)
        
    class Meta:
        verbose_name = "Temoignage"
        verbose_name_plural = "Temoignages"
        
    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return reverse('temoignage_detail', args=[str(self.id)])
    
    @property
    def full_name (self):
        return f'{self.first_name}-{self.last_name}'

class ProgrammeHebdo(models.Model):
    JOUR_CHOICES = [
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi', 'Samedi'),
        ('dimanche', 'Dimanche'),
    ]
    
    jour = models.CharField(max_length=10, choices=JOUR_CHOICES)
    horaire = models.CharField(max_length=20)
    activite = models.CharField(max_length=100)
    icone = models.CharField(max_length=50, default="fa-solid fa-hands-praying")
    badge_special = models.BooleanField(default=False)
    salle = models.CharField(max_length=50)
    responsable = models.CharField(max_length=100)
    ordre = models.PositiveIntegerField(default=0, help_text="Pour trier les activités")
    
    class Meta:
        verbose_name = "Programme Hebdo"
        verbose_name_plural = "Programmes Hebdo"

    def __str__(self):
        return f"{self.jour} - {self.activite}"

class LiveStream(models.Model, VideoMixin):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
    ]
    
    titre = models.CharField(max_length=200, default="Culte en Direct")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='youtube')
    url = models.URLField(help_text="URL du flux (ex: YouTube Live)")
    is_live = models.BooleanField(default=False, help_text="Activer si le direct est en cours")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Direct"
        verbose_name_plural = "Direct"

    def __str__(self):
        return self.titre
    
    def clean(self):
        if not self.url:
            raise ValidationError("L'URL est requise")
        
        embed_url = self.get_embed_url()
        if not embed_url:
            raise ValidationError("L'URL fournie n'est pas reconnue ou n'est pas supportée.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('live_stream_detail', args=[str(self.id)])

class Video(models.Model, VideoMixin):
    """Modèle générique pour ajouter des vidéos à n'importe quel contenu."""
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('facebook', 'Facebook'),
        ('vimeo', 'Vimeo'),
        ('tiktok', 'TikTok'),
    ]
    
    titre = models.CharField(max_length=200)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='youtube')
    url = models.URLField(help_text="Collez l'URL de la vidéo ici")
    
    # Generic Relation pour lier à Predication, Evenement ou autre
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vidéo"
        verbose_name_plural = "Vidéos"

    def __str__(self):
        return self.titre

    def clean(self):
        if self.url and not self.get_embed_url():
            raise ValidationError("URL de vidéo invalide ou plateforme non supportée.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Gallery(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Galerie"
        verbose_name_plural = "Galeries"
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Image {self.id}"
