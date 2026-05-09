from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import LiveStream, Predication, Evenement, ProgrammeHebdo, Temoignages, Video, Gallery

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image_preview', 'created_at']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "Pas d'image"
    image_preview.short_description = "Aperçu"

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['titre', 'platform', 'created_at', 'video_preview']
    list_filter = ['platform', 'created_at']
    search_fields = ['titre', 'url']
    readonly_fields = ['video_preview']

    def video_preview(self, obj):
        url = obj.get_embed_url()
        if url:
            # Petit aperçu pour l'admin
            return mark_safe(f'<iframe width="320" height="180" src="{url}" frameborder="0" allowfullscreen></iframe>')
        return "Aperçu non disponible"
    video_preview.short_description = "Aperçu"

@admin.register(Predication)
class PredicationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'predicateur', 'date']
    search_fields = ['titre', 'predicateur', 'resume']
    list_filter = ['date', 'theme']
    prepopulated_fields = {'slug': ('titre',)}

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date', 'lieu']
    list_filter = ['name', 'date']
    search_fields = ['name', 'description']
    list_per_page = 25
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Temoignages)
class TemoignagesAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'published']
    search_fields = ['first_name', 'last_name']
    list_filter = ['published']
    list_per_page = 25

@admin.register(ProgrammeHebdo)
class ProgrammeHebdoAdmin(admin.ModelAdmin):
    list_display = ['jour', 'horaire', 'activite', 'salle', 'responsable']
    list_filter = ['jour', 'badge_special']
    ordering = ['ordre']
    list_per_page = 25

@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ['titre', 'url', 'is_live', 'updated_at', 'video_preview']
    list_editable = ['is_live', 'url']
    readonly_fields = ['video_preview']

    def video_preview(self, obj):
        url = obj.get_embed_url()
        if url:
            return mark_safe(f'<iframe width="320" height="180" src="{url}" frameborder="0" allowfullscreen></iframe>')
        return "Aperçu non disponible"
    video_preview.short_description = "Aperçu Direct"
