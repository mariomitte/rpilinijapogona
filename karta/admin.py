from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

from . import models as karte_models


admin.site.register(karte_models.HQ, LeafletGeoAdmin)
