from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pogon1'

from .views import (
    # admin metode
    upravljanje_list,
    upravljanje_create,
    upravljanje_detail,
    upravljanje_update,
    upravljanje_delete,

    # operater metode
    pogon,
    dokumentacija,
    upravljanje_prijava,
    upravljanje_odjava,
    )

urlpatterns = [

    # dodaj obavijesti
    url(r'^list/$', upravljanje_list, name='list'),
    url(r'^create/$', upravljanje_create, name='create'),
    url(r'^(?P<id>\d+)/$', upravljanje_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', upravljanje_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', upravljanje_delete, name='delete'),

    # linija pogona
    # /pogon/
    url(r'^$', pogon, name='pogon'),
    # /pogon/dokumentacija
    url(r'^dokumentacija/$', dokumentacija, name='dokumentacija'),
    # /pogon/prijava
    url(r'^prijava/$', upravljanje_prijava, name='prijava'),
    # /pogon/odjava
    url(r'^odjava/$', upravljanje_odjava, name='odjava'),
]
