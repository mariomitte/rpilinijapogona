from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from pogon1.api.views import UpravljanjeViewSet, CvorViewSet

router = DefaultRouter()
router.register(prefix='upravljanje', viewset=UpravljanjeViewSet)

urlpatterns = [
    url(r'^cvor/$', CvorViewSet.as_view()),
]

urlpatterns += router.urls
