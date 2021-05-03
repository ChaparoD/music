from django.db import models

# Create your models here.

# Create your models here.


class Artista(models.Model):
    id = models.CharField(max_length=23, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    albums = models.URLField()
    tracks = models.URLField()
    self_a = models.URLField()


class Album(models.Model):
    id = models.CharField(max_length=23, primary_key=True)
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    artist = models.URLField()
    tracks = models.URLField()
    self_u = models.URLField()


class Cancion(models.Model):
    id = models.CharField(max_length=23, primary_key=True)
    name = models.CharField(max_length=100)
    duration = models.FloatField()
    times_played = models.IntegerField()
    artist = models.URLField()
    album = models.URLField()
    self_c = models.URLField()