from rest_framework import serializers
from pogon1.models import Upravljanje


class UpravljanjeSerializer(serializers.ModelSerializer):
    """ Serializer za operatera """
    class Meta:
        model = Upravljanje
        fields = ('korisnik', 'title', 'content', 'image')


class CvorSerializer(serializers.ModelSerializer):
    """ Serializer za cvor """
    class Meta:
        model = Upravljanje
        fields = ('korisnik', 'kod', 'model', 'extra')
