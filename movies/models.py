from django.db import models
from utils.models import TimeStampMixin


class Genre(TimeStampMixin):
    name = models.CharField(max_length=255, unique=True, verbose_name='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Person(TimeStampMixin):
    external_id = models.CharField(max_length=20, unique=True, verbose_name='IMDb ID')
    name = models.CharField(max_length=255, verbose_name='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'


class Movie(TimeStampMixin):
    external_id = models.CharField(max_length=20, unique=True, verbose_name='IMDb ID')
    title = models.CharField(max_length=255, verbose_name='Title')
    score = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Score')
    synopsis = models.TextField(verbose_name='Synopsis')
    year = models.PositiveSmallIntegerField(verbose_name='Year')
    duration = models.TimeField(verbose_name='Duration')
    genres = models.ManyToManyField(Genre, verbose_name='Genres')
    cover = models.URLField(verbose_name='Cover')
    directors = models.ManyToManyField(Person, related_name='+', verbose_name='Directors')
    actors = models.ManyToManyField(Person, related_name='+', verbose_name='Actors')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class ImportMovie(models.Model):

    class Meta:
        verbose_name = 'Import Movie'
        verbose_name_plural = 'Import Movie'
