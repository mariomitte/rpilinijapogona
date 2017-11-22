from django.contrib import admin
from .models import Upravljanje

class UpravljanjeModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated', 'timestamp', 'model', 'mcu', 'kod', 'extra')
    list_display_links = ('updated',)
    list_editable = ('title',)
    list_filter = ('updated', 'timestamp', 'mcu')
    search_fields = ('title', 'content', 'model', 'kod')
    class Meta:
        model = Upravljanje


# Register your models here.
#admin.site.register(Upravljanje, CvorModelAdmin)
admin.site.register(Upravljanje, UpravljanjeModelAdmin)
