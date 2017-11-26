"""linijapogona URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [

    # /welcome/
    url(r'^$', TemplateView.as_view(template_name='welcome.html'), name='welcome'),

    # /admin/
    url(r'^admin/', admin.site.urls),

    # /api/
    url(r'^api/', include('pogon1.api.urls')),

    # /pogon1/
    url(r'^pogon1/', include('pogon1.urls', namespace='pogon1')),

    # /pogon2/
    #url(r'^pogon2/', include('pogon2.urls', namespace='pogon2')),

    # /pogon3/
    #url(r'^pogon3/', include('pogon3.urls', namespace='pogon3')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
