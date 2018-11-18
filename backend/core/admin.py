from django.contrib import admin

from core import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('group', 'status', 'description', 'link', 'location',
                    'created', 'modified')
    search_fields = ('group', 'status', 'description')
    readonly_fields = ('created', 'modified')


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'links',)
    search_fields = ('name', 'logo', 'links',)
