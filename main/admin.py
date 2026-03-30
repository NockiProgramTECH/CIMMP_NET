from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Predication, Evenement,Temoignages

admin.site.register(Predication)
# @admin.register(Predication)
# class PredicationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'orateur','date']
#     search_fields = ['name', 'description', 'orateur','date']
#     list_per_page = 25
#     readonly_fields = ['date']
#     # fieldsets = (
#     #     (None, {
#     #         'fields': ('name', 'description')
#     #     }),
#     #     ('Advanced options', {
#     #         'classes': ('collapse',),
#     #         'fields': ('is_active', 'metadata'),
#     #     }),
#     # )
@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
        list_display = ['id', 'name', 'date']
        list_filter = ['name', 'date']
        search_fields = ['name', 'date']
        list_per_page = 25
        # fieldsets = (
        #     (None, {
        #         'fields': ('name', 'description')
        #     }),
        #     ('Advanced options', {
        #         'classes': ('collapse',),
        #         'fields': ('is_active', 'metadata'),
        #     }),
        # )


@admin.register(Temoignages)
class TemoignagesAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name']
    search_fields = ['first_name','last_name']
    list_per_page = 25
   
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'description')
    #     }),
    #     ('Advanced options', {
    #         'classes': ('collapse',),
    #         'fields': ('is_active', 'metadata'),
    #     }),
    # )