from django.conf.urls import url
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView

from .models import HQ
from .views import HelloPDFView

app_name = 'karta'

urlpatterns = [
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=HQ), name='data'),
    url(r'^$', TemplateView.as_view(template_name='karta/karta.html'), name='karta'),
#    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=HQ, properties=('title', 'description', 'picture_url')), name='data')
    url(r'^lopud.pdf$', HelloPDFView.as_view())
]
