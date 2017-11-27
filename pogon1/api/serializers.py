from rest_framework import serializers
from pogon1.models import Upravljanje

# Povezuje model i pogled: cjelokupni model
# Ovdje se uređuju detalji modela koji su prikazani korisniku u pogledu
class UpravljanjeSerializer(serializers.ModelSerializer):
    """ Serializer za operatera """
    class Meta:
        model = Upravljanje
        fields = ('korisnik', 'title', 'kod', 'model', 'extra')

# Povezuje model i pogled: API Telegram
# Ovdje se uređuju detalji modela koji su prikazani korisniku u pogledu
class CvorSerializer(serializers.ModelSerializer):
    """ Serializer za cvor """
    class Meta:
        model = Upravljanje
        fields = ('korisnik', 'kod', 'model', 'extra')
