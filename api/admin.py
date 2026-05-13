from django.contrib import admin
from .models import RendezVous, AppVersion

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_rdv', 'status', 'created_at')
    list_filter = ('status', 'date_rdv')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'is_active', 'force_update', 'created_at')
    list_filter = ('is_active', 'force_update')
    search_fields = ('version',)
