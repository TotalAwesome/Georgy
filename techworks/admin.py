from django.contrib import admin
from techworks.models import TechWork, TechWorkSource
# Register your models here.

class TechWorkSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active')
    list_editable = ('url', 'is_active')


class TechWorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'title', 'time_string', 'start_time', 'end_time', 'new')
    list_display_links = ('title',)
    list_editable = ('new',)

admin.site.register(TechWorkSource, TechWorkSourceAdmin)
admin.site.register(TechWork, TechWorkAdmin)