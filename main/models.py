
from os import name
from pyexpat import model

from django.db import models
from django.urls import reverse
from django.utils import timezone


class Predication(models.Model):
    # Informations principales
    img_couverture=models.ImageField(upload_to ='predications/')
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    date = models.DateTimeField()
    url_video =models.URLField(blank=True)
    audio =models.FileField(upload_to="audio",blank=True,null=True) # lien vers la vidéo de la prédication
    resume = models.TextField(blank=True)
    verset_principal = models.CharField(max_length=100, blank=True)
    contenu = models.TextField(blank=True)  # texte complet ou lien vidéo/audio

    # Relations
    predicateur = models.CharField("Preacher", max_length=200)
    interprete = models.CharField("Interprete", max_length=200, null=True, blank=True)

    # Catégorisation
    theme = models.CharField(max_length=100, blank=True)  # ex: Foi, Prière, Prophétie

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metadata
    class Meta:
        verbose_name = "Predication"
        verbose_name_plural = "Predications"
        ordering = ['date']
    
    # Methods
    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.titre.lower().replace(" ", "-")
        super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        return reverse('predication_detail', args=[str(self.slug)])

    # Properties

class Evenement(models.Model):
    """Models pour les evenements"""
    
    # Fields
    name = models.CharField(max_length=100)
    slug =models.SlugField(unique=True)
    description = models.TextField()
    date =models.DateTimeField()
    lieu =models.CharField(max_length =25,default ="Eglise CIMPP")
    image = models.ImageField(upload_to='evenements/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metadata
    class Meta:
        verbose_name = "Evenement"
        verbose_name_plural = "Evenements"
        ordering = ['name']
    
    # Methods
    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(" ", "-")
        super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        return reverse('evenement_detail', args=[str(self.slug)])

class Temoignages(models.Model):
    """Model temognage"""
        # Fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone =models.CharField(max_length =10)
    subjet =models.CharField(max_length=50)
    temoignage =models.TextField()
    created_at  =models.DateTimeField(auto_created=True,default=timezone.now)
    published =models.BooleanField(default=False)
        
        # Metadata
    class Meta:
            verbose_name = "Temoignage"
            verbose_name_plural = "Temoignages"
            # ordering = ['name']
        
        # Methods
    def __str__(self):
            return self.full_name
        
    def get_absolute_url(self):
            return reverse('temoignage_detail', args=[str(self.id)])
    
        # Properties
    @property
    def full_name (self):
            return f'{self.first_name}-{self.last_name}'
    