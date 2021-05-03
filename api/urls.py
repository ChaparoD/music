from django.urls import path
from . import views


urlpatterns =[
path("", views.index, name="index"),


path("artists/<str:id>/tracks", views.ArtistaDetailTracks, name="artists-detail-tracks"), 
path("albums/", views.AlbumList, name="albums"),
path("tracks/", views.CancionList, name="tracks"),



path("artists/", views.ArtistMethods.as_view(), name="artist-get-create"),#CHECK  #get y create generales #path("artists/", views.ArtistaCreate, name = "artists-create"),  

path("artists/<str:id>", views.ArtistMethods_id.as_view(), name="artists-get-delete"),#CHECK  #get y delete artis-id path("artists/<str:id>", views.ArtistaDelete, name="artists-delete"),

path("artists/<str:id>/albums", views.ArtistMethos_forAlbums.as_view(), name="artist-albums-get-create"), #get albums y create path("artists/<str:id>/albums", views.AlbumCreate, name = "artist-album-create"),

path("albums/<str:id>", views.AlbumMethods_id.as_view(), name="albums-get-delete"),      #get y delete         #gets individuales para album

path("albums/<str:id>/tracks", views.AlbumMethods_forTracks.as_view(), name="albums-get-create-tracks"), #get canciones y create cancion path("albums/<str:id>/tracks", views.CancionCreate, name = "album-track-create"),

path("tracks/<str:id>", views.CancionMethods.as_view(), name="tracks-get-delete"),   # get y delete cancion path("tracks/<str:id>", views.CancionDelete, name="albums-delete"),
]