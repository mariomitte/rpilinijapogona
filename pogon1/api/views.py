from rest_framework import viewsets, generics
from pogon1.models import Upravljanje
from pogon1.api.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from pogon1.api import serializers

# Django rest_framework API response
class PogonApiView(APIView):
    """Test API View."""

    # dodaj serializers varijablu i referenciraj ju
    serializers_class = serializers.UpravljanjeSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    # metoda za POST response
    def post(self, request):
        """Create a hello message with our name."""

        serializer = serializers.UpravljanjeSerializer(data=request.data) # što god da request ima pošalji serializer objektu

        # provjeri da serializer ima ispravni data
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name) # {0, 1, 2} to je red po kojemu želim izlistati message koji je upisao korisnik
            return Response({'message': message})

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST) # sadrži lista grešaka koji nastanu

    # Http response
    def put (self, request, pk=None):
        """Handles updating object."""

        return Response({'method': 'put'})

    # Partialy update object
    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """Delete an object."""

        return Response({'method':'delete'})

class UpravljanjeViewSet(viewsets.ModelViewSet):
    queryset = Upravljanje.objects.all()
    serializer_class = UpravljanjeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)

class CvorViewSet(generics.ListAPIView):
    serializer_class = CvorSerializer
    permission_classes = (AllowAny,)
    def get_queryset(self):
        queryset = Upravljanje.objects.all()
        kod_id = self.request.query_params.get('kod', None)
        queryset = queryset.filter(kod='pogon1')
        return queryset
