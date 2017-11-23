# django core
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.urlresolvers import reverse
from kamera.kamera_stream import *

#picamera
camera = CameraNetwork()

# media/<user>
def upload_location(instance, filename):
    return '%s/%s' %(instance.korisnik, filename)

# modeli
class Upravljanje(models.Model):
    # korisnik
    korisnik = models.ForeignKey(User, default=1)

    # ostali detalji modela
    title = models.CharField(max_length=120)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.FileField(upload_to=upload_location, null=True, blank=True)
    user_in = models.BooleanField(default=False)

    # API
    kod = models.CharField(max_length=64, blank=False)
    mcu = models.CharField(max_length=500)
    model = models.CharField(max_length=500)
    extra = models.CharField(max_length=500)

    def __str__(self):
        'Operater {}: {} - {}'.format(self.korisnik, self.title, self.user_in)

    def get_absolute_url(self):
        return reverse('pogon1:detail', kwargs={'id':self.id})

    def check_exists_device(kod_id):
        # Izradi kod ukoliko ne postoji

        if not Cvor.objects.filter(kod=kod_id):
            kreirao = User.objects.filter(username="linijapogona").first()
            kod_create = Cvor.objects.create(user=kreirao, kod=kod_id)

    class Meta:
        ordering = ['-timestamp', '-updated']
