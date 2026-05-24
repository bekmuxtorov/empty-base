from django.contrib import admin
from .models import (
    DataRecord, BKGazCurrentData, BKGazHourlyArchive, 
    BKGazDailyArchive, BKGazMonthlyArchive, BKGazEmergencyArchive, 
    BKGazVariableArchive
)

class FormattedTimestampMixin:
    @admin.display(description='Vaqt', ordering='timestamp')
    def formatted_timestamp(self, obj):
        if getattr(obj, 'timestamp', None):
            try:
                return obj.timestamp.strftime('%Y-%m-%d %H:%M')
            except AttributeError:
                return obj.timestamp
        return "-"

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

@admin.register(BKGazCurrentData)
class BKGazCurrentDataAdmin(admin.ModelAdmin, FormattedTimestampMixin):
    list_display = ('device_address', 'formatted_timestamp', 'work_volume', 'std_volume', 'pressure', 'temperature', 'emergency_active', 'created_at')
    list_filter = ('emergency_active', 'device_address', 'timestamp')
    search_fields = ('device_address',)
    ordering = ('-timestamp',)

@admin.register(BKGazHourlyArchive)
class BKGazHourlyArchiveAdmin(admin.ModelAdmin, FormattedTimestampMixin):
    list_display = ('device_address', 'formatted_timestamp', 'pressure', 'temperature', 'acc_work_vol', 'acc_std_vol')
    list_filter = ('device_address', 'timestamp')
    search_fields = ('device_address',)
    ordering = ('-timestamp',)

@admin.register(BKGazDailyArchive)
class BKGazDailyArchiveAdmin(admin.ModelAdmin, FormattedTimestampMixin):
    list_display = ('device_address', 'formatted_timestamp', 'work_vol', 'std_vol', 'acc_work_vol', 'acc_std_vol')
    list_filter = ('device_address', 'timestamp')
    search_fields = ('device_address',)
    ordering = ('-timestamp',)

@admin.register(BKGazMonthlyArchive)
class BKGazMonthlyArchiveAdmin(admin.ModelAdmin, FormattedTimestampMixin):
    list_display = ('device_address', 'formatted_timestamp', 'work_vol', 'std_vol', 'acc_work_vol', 'acc_std_vol')
    list_filter = ('device_address', 'timestamp')
    search_fields = ('device_address',)
    ordering = ('-timestamp',)

@admin.register(BKGazEmergencyArchive)
class BKGazEmergencyArchiveAdmin(admin.ModelAdmin, FormattedTimestampMixin):
    list_display = ('device_address', 'formatted_timestamp', 'code_word', 'changed', 'value')
    list_filter = ('changed', 'device_address', 'code_word')
    search_fields = ('device_address',)
    ordering = ('-created_at',)

@admin.register(BKGazVariableArchive)
class BKGazVariableArchiveAdmin(admin.ModelAdmin, FormattedTimestampMixin):
    list_display = ('device_address', 'formatted_timestamp', 'gas_density', 'baro_pressure', 'max_flow', 'min_flow')
    list_filter = ('device_address', 'timestamp')
    search_fields = ('device_address',)
    ordering = ('-timestamp',)
