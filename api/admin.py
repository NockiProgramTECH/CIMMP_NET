from django.contrib import admin
from .models import RendezVous

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_rdv', 'status', 'created_at')
    list_filter = ('status', 'date_rdv')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
