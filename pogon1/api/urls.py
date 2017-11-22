from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from pogon1.api.views import CvorViewSet

router = DefaultRouter()
router.register('cvor', CvorViewSet)

urlpatterns = [
    #
]

urlpatterns += router.urls
