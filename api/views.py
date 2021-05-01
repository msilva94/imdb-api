from django.db.models import Q
from django.shortcuts import render
from movies.models import Movie, Person
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import (MovieListSerializer, MovieSerializer,
                          PersonListSerializer, PersonSerializer)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()

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

        return queryset.order_by('-score')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieSerializer

        return MovieListSerializer


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()

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
