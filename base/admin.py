from django.contrib import admin
from .models import DataRecord

@admin.register(DataRecord)
class DataRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'meter_id', 'status', 'pressure', 'temperature', 'volume', 'battery', 'signal', 'timestamp')
    list_display_links = ('id', 'device_id')
    search_fields = ('device_id', 'meter_id', 'phone', 'status')
    list_filter = ('status', 'device_id', 'timestamp')
    ordering = ('-timestamp', '-created_at')
    
    fieldsets = (
        ('Device Identity', {
            'fields': (('device_id', 'meter_id'), 'phone'),
            'description': 'Information about the device and connectivity.'
        }),
        ('Measurement Data', {
            'fields': ('pressure', 'temperature', 'volume'),
            'description': 'Actual measurement values.'
        }),
        ('Technical Status', {
            'fields': (('signal', 'battery'), 'status'),
            'description': 'Current signal strength, battery level, and status.'
        }),
        ('Time Stamps', {
            'fields': ('timestamp', 'created_at'),
            'description': 'Event timestamps recorded by the device.'
        }),
    )

    readonly_fields = ('created_at',)

    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }
