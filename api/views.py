from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse  ##se supone que ahora no utilizaré los http response

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers
from .serializers import ArtistaSerializer, AlbumSerializer, CancionSerializer
from .models import Artista, Album, Cancion
from base64 import *
from rest_framework import status
import json

# Create your views here.

#hay que codificar el identificador con base64 


@api_view(['GET', 'POST'])
def index(response):
    api_urls = {
        'List (GET)': '/artists/',
        'Detail View (GET)': '/artists/id/',
        'Delete View (DELETE)': '/artists/id/',
        'List View (GET)': 'artists/id/albums/',
        'Create (POST)':'/artists/',

        'List (GET)': '/albums/',
        'Detail View (GET)': '/albums/id/',
        'Delete View (DELETE)': '/albums/id/',
        'Create (POST)':'artist/id/albums/',
        'View (GET)': '/albums/id/tracks',
        


        'List (GET)': '/tracks/',
        'Detail View (GET)': '/tracks/id/',
        'Delete View (DELETE)': '/tracks/id/',
        'Create (POST)': '/albums/id/tracks',


        
    }

    return Response(api_urls)



#==================-------------================== 
#===================  urls individuales ================== 


# artist/id/tracks
@api_view(['GET'])
def ArtistaDetailTracks(request, id):
    try:
        artista = Artista.objects.get(id = id)
        canciones = Cancion.objects.filter(artist = artista.self_a)
        return Response({}, status = status.HTTP_409_CONFILCT)
    except:
        pass

    artista = Artista.objects.get(id = id)
    tracks = Cancion.objects.filter(artist = artista.self_a)
    response = []
    for track in tracks:
        datos = (track.id, track.name, track.duration, track.times_played, track.artist, track.album, track.self_c)
        keys = ("id", "name", "duration", "times_played", "artist", "album","self_c")
        response_dict = dict(zip(keys, datos))
        response.append(response_dict)
    
    return Response(response)

# albums/ (LISTO)
@api_view(['GET'])
def AlbumList(request):
    try:
        albunes = Artista.objects.all()
        return Response({}, status = status.HTTP_409_CONFILCT)
    except:
        pass

    albunes = Album.objects.all()
    response = []
    for album in albunes:
        datos = (album.id, album.name, album.genre, album.artist, album.tracks, album.self_u)
        keys = ("id", "name", "genre", "artist", "tracks", "self_u")
        response_dict = dict(zip(keys, datos))
        response.append(response_dict)

    return Response(response)
    
# tracks/ (LISTO)
@api_view(['GET'])
def CancionList(request):
    try:
        albunes = Cancion.objects.all()
        return Response({}, status = status.HTTP_409_CONFILCT)
    except:
        pass
    tracks = Cancion.objects.all()
    response = []
    for track in tracks:
        datos = (track.id, track.name, track.duration, track.times_played, track.artist, track.album, track.self_c)
        keys = ("id", "name", "duration", "times_played", "artist", "album","self_c")
        response_dict = dict(zip(keys, datos))
        response.append(response_dict)
    
    return Response(response)

#==================-------------================== 
#===================  urls con != metodologías ================== 

# /artist (LISTO)
class ArtistMethods(APIView):
    serializer_class = serializers.ArtistaSerializer



    def get(self, request):
        artistas = Artista.objects.all()
        response = []
        for artist in artistas:
            datos = (artist.id, artist.name, artist.age, artist.albums, artist.tracks, artist.self_a)
            keys = ("id", "name", "age", "albums", "tracks", "self_a")
            response_dict = dict(zip(keys, datos))
            response.append(response_dict)
        serializado = json.dumps(response)
        return Response(response)


    def post(self, request):
        serializer = self.serializer_class(data=request.data)  #no habría que linkearlo con nada

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            age = serializer.validated_data.get('age')
            new_id = b64encode(name.encode()).decode()[0:22]
            print(new_id)
            try:
                existe = Artista.objects.get(id = new_id)
                return Response({}, status = status.HTTP_409_CONFILCT)
            except:
                pass

            artist = Artista()
            artist.name = name
            artist.id = new_id
            artist.age = age
            artist.self_a = f"http://127.0.0.1:8000/artists/{artist.id}"
            artist.albums = f"http://127.0.0.1:8000/artists/{artist.id}/albums"
            artist.tracks = f"http://127.0.0.1:8000/artists/{artist.id}/tracks"
            
            datos = (artist.id, artist.name, artist.age, artist.albums, artist.tracks, artist.self_a)
            keys = ("id", "name", "age", "albums", "tracks", "self_a")
            response_dict = dict(zip(keys, datos))
            print(response_dict)
            artist.save()
             
            return Response([response_dict], status = status.HTTP_201_CREATED)
            
        else:
            return Response(serializer.errors,
            status = status.HTTP_400_BAD_REQUEST)

#/artist/id  (LISTO)
class ArtistMethods_id(APIView):
    

    def get(self, request, id):
        try:
            artist = Artista.objects.get(id = id )
            return Response({}, status = status.HTTP_409_CONFILCT)
        except:
            pass
        artist = Artista.objects.get(id = id )
        keys = ("id", "name", "age", "albums", "tracks", "self_a")
        datos = (artist.id, artist.name, artist.age, artist.albums, artist.tracks, artist.self_a)
        response_dict = dict(zip(keys, datos))
        return Response(response_dict)
    
   
    def delete(self, request, id):
        try:
            existe = Artista.objects.get(id = id)
            return Response({}, status = status.HTTP_409_CONFILCT)
        except:
            pass
        artista = Artista.objects.get(id = id)
        albunes = Album.objects.filter(artist = artista.self_a)
        for album in albunes:
            AlbumMethods_id.delete(self, "albums/<str:id>", album.id)
        artista.delete()    #agregar eliminacion en cascada de todos sus albums - elimina todas las canciones del albums

        return Response({}, status = status.HTTP_204_NO_CONTENT)

#artist/id/albums (LISTO)
class ArtistMethos_forAlbums(APIView):
    serializer_class = serializers.AlbumSerializer
    print("entro a la clase")

    def get(self, request, id):
        try:
            artista = Artista.objects.get(id = id )
            albums_artista = Album.objects.get(artist = artista.self_a )   #ver esto pq artist tiene url de sus albums
            return Response({}, status = status.HTTP_409_CONFILCT)
        except:
            pass

        artista = Artista.objects.get(id = id )
        albums_artista = Album.objects.filter(artist = artista.self_a)
        print(albums_artista)
        resultado =[]
        for album in albums_artista:
            datos = (album.id, album.name, album.genre, album.artist, album.tracks, album.self_u)
            keys = ("id", "name", "genre", "artist", "tracks", "self_u")
            response_dict = dict(zip(keys, datos))
            resultado.append(response_dict)
        
        return Response(resultado)

    

    def post(self, request, id):
        
        serializer = self.serializer_class(data=request.data)   #hay que linkearlo al artista.
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            genre = serializer.validated_data.get('genre')
            new_id = b64encode(name.encode()).decode()[0:22]
            print(new_id)
            try:
                existe = Album.objects.get(id = new_id)
                artista = Artista.objects.get(id = id )
                return Response({}, status = status.HTTP_409_CONFILCT)
            except:
                pass
            
            artista = Artista.objects.get(id = id )
            album = Album()
            album.name = name
            album.id = new_id
            album.genre = genre
            album.self_u = f"http://127.0.0.1:8000/albums/{album.id}"
            album.artist = artista.self_a
            album.tracks = f"http://127.0.0.1:8000/albums/{album.id}/tracks"
            
            datos = (album.id, album.name, album.genre, album.artist, album.tracks, album.self_u)
            keys = ("id", "name", "genre", "artist", "tracks", "self_u")
            response_dict = dict(zip(keys, datos))
            print(response_dict)
            album.save()
             
            return Response(response_dict, status = status.HTTP_201_CREATED)
            
        else:
            return Response(serializer.errors,
            status = status.HTTP_400_BAD_REQUEST)


# albums/id (LISTO - ver si funciona delete)

class AlbumMethods_id(APIView):


    def get(self, request, id):
        try:
            artist = Album.objects.get(id = id )
            return Response({}, status = status.HTTP_409_CONFILCT)
        except:
            pass
        
        album = Album.objects.get(id = id )
        datos = (album.id, album.name, album.genre, album.artist, album.tracks, album.self_u)
        keys = ("id", "name", "genre", "artist", "tracks", "self_u")
        response_dict = dict(zip(keys, datos))
        return Response(response_dict)


    def delete(self, request, id):
        try:
            existe = Album.objects.get(id = id)
            return Response({}, status = status.HTTP_409_CONFILCT)
        except:
            pass
        album = Album.objects.get(id = id)
        canciones = Cancion.objects.filter(album = album.self_u)
        for cancion in canciones:
            CancionMethods.delete(self, "tracks/<str:id>", cancion.id)
        
        album.delete()    #agregar eliminacion en cascada de todos sus albums - elimina todas las canciones del albums

        return Response({}, status = status.HTTP_204_NO_CONTENT)


# albums/id/tracks
class AlbumMethods_forTracks(APIView):
    serializer_class = serializers.CancionSerializer
    
    def get(self, request, id):
        try:
            albun = Album.objects.get(id = id)
            artist = Cancion.objects.get(album = albun.self_u)
            return Response({}, status = status.HTTP_409_CONFILCT)
        except:
            pass
        
        album = Album.objects.get(id = id )
        tracks = Cancion.objects.filter(album = album.self_u)    #ver esta wea dsp pq e album tiene el link de sus tracks
        response = []
        for track in tracks:
            datos = (track.id, track.name, track.duration, track.times_played, track.artist, track.album, track.self_c)
            keys = ("id", "name", "duration", "times_played", "artist", "album", "self_c")
            response_dict = dict(zip(keys, datos))
            response.append(response_dict)

        return Response(response)
 

    
    def post(self, request, id):
        
        serializer = self.serializer_class(data=request.data)   #hay que linkearlo al artista.
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            duration = serializer.validated_data.get('duration')
            times_played = serializer.validated_data.get('times_played')
            new_id = b64encode(name.encode()).decode()[0:22]
            print(new_id)
            print(times_played)
            try:
                existe = Album.objects.get(id = id)
                exi = Cancion.objects.get(id = new_id)
                return Response({}, status = status.HTTP_409_CONFILCT)
            except:
                pass

            album = Album.objects.get(id = id)
            artist = Artista.objects.get(self_a = album.artist)

            track = Cancion()
            track.name = name
            track.id = new_id
            track.duration = duration
            track.times_played = times_played
            track.self_c = f"http://127.0.0.1:8000/tracks/{track.id}"
            track.album = album.self_u
            track.artist = artist.self_a
            track.save()
            
            datos = (track.id, track.name, track.duration, track.times_played, track.artist, track.album, track.self_c)
            keys = ("id", "name", "duration", "times_played", "artist", "album","self_c")
            response_dict = dict(zip(keys, datos))
            

             
            return Response(response_dict, status = status.HTTP_201_CREATED)
            
        else:
            return Response(serializer.errors,
            status = status.HTTP_400_BAD_REQUEST)



#tracks/id  (LISTO)
class CancionMethods(APIView):


    def get(self, request, id):
        try:
            cancion = Cancion.objects.get(id = id )
            albums_artista = Album.objects.filter(artist = cancion.artist )   #ver esto pq artist tiene url de sus albums
            artistas = Artista.objects.get(self_a = cancion.artist)
            return Response({}, status = status.HTTP_409_CONFILCT)
        except:
            pass

        track = cancion.objects.get(id = id )
        datos = (track.id, track.name, track.duration, track.times_played, track.artist, track.self_c)
        keys = ("id", "name", "duration", "times_played", "artist", "self_c")
        response_dict = dict(zip(keys, datos))
        
        return Response(response_dict)


    
    def delete(self, request, id):
        try:
            existe = Cancion.objects.get(id = id)
            return Response({}, status = status.HTTP_409_CONFILCT)
        except:
            pass
        cancion= Cancion.objects.get(id = id)
        cancion.delete()    #agregar eliminacion en cascada de todos sus albums - elimina todas las canciones del albums

        return Response({}, status = status.HTTP_204_NO_CONTENT)

