from rest_framework import viewsets
from . import models
from . import serializers


class ArtistaViewset(viewsets.ModelViewSet):
    queryset = models.Artista.objects.all()
    serializer_class = serializers.ArtistaSerializer  #serializer class initialization usamos esto para serializar

# acá creamos funciones que nos permitan trabajar con los datos List(), retrieve, create (), update(), destroy(), etccc
#acá debemos mapear los urls para que trabajen los datos. (routing)

class AlbumViewset(viewsets.ModelViewSet):
    queryset = models.Album.objects.all() #accedemos a todos los atributos del modelo.
    serializer_class = serializers.AlbumSerializer


class CancionViewSet(viewsets.ModelViewSet):
    queryset = models.Cancion.objects.all()
    serializer_class = serializers.CancionSerializer