from rest_framework import serializers
from .models import Artista, Album, Cancion

class ArtistaSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(default=0)



class AlbumSerializer(serializers.Serializer):

    
    name = serializers.CharField(max_length=100)
    genre = serializers.CharField(max_length=100)


class CancionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    duration = serializers.FloatField()
    times_played = serializers.FloatField()
