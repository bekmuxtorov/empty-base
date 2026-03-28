from django.contrib import admin
from .models import DataRecord

@admin.register(DataRecord)
class DataRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'field1', 'field2', 'field3', 'field4', 'field5')
    list_display_links = ('id', 'field1')
    search_fields = ('field1', 'field2', 'field3', 'field4', 'field5')
    list_filter = ('field1', 'field2')
    
    fieldsets = (
        ('Summary Information', {
            'fields': ('field1', 'field2','field3', 'field4', 'field5'),
            'description': 'Main data details.'
        }),
        )

    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }
