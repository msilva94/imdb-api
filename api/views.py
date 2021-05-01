from django.db.models import Q
from django.shortcuts import render
from movies.models import Movie, Person
from rest_framework import filters, viewsets
from rest_framework.response import Response

from .filters import MinLengthSearchFilter, MovieOrderingFilter
from .serializers import (MovieListSerializer, MovieSerializer,
                          PersonListSerializer, PersonSerializer)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    filter_backends = [MinLengthSearchFilter, MovieOrderingFilter]
    ordering_fields = ['title', 'score', 'year']
    ordering = ['-score', 'title']
    search_fields = ['title', '=external_id']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieSerializer

        return MovieListSerializer


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    filter_backends = [MinLengthSearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PersonSerializer

        return PersonListSerializer
