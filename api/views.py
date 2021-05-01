from django.db.models import Q
from django.shortcuts import render
from movies.models import Movie, Person
from rest_framework import filters, viewsets
from rest_framework.response import Response

from .filters import MovieOrderingFilter
from .serializers import (MovieListSerializer, MovieSerializer,
                          PersonListSerializer, PersonSerializer)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    filter_backends = [MovieOrderingFilter]
    ordering_fields = ['title', 'score', 'year', 'duration']
    ordering = ['-score', 'title']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'retrieve':
            return queryset

        q = self.request.query_params.get('q', None)
        if q:
            if len(q) < 3:
                return queryset.none()
            queryset = queryset.filter(Q(title__icontains=q) | Q(external_id=q))
            return queryset

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieSerializer

        return MovieListSerializer


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'retrieve':
            return queryset
        
        q = self.request.query_params.get('q', None)
        if q:
            if len(q) < 3:
                return queryset.none()
            queryset = queryset.filter(name__icontains=q)
            return queryset
        
        return queryset.none()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PersonSerializer

        return PersonListSerializer
