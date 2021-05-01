from movies.models import Movie, Person, Genre
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['id', 'name']


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id', 'title', 'score', 'year', 'cover']


class DurationSerializer(serializers.Serializer):
    hours = serializers.IntegerField(source='hour')
    minutes = serializers.IntegerField(source='minute')

    class Meta:
        fields = ['hours' ,'minutes']


class MovieSerializer(serializers.ModelSerializer):
    duration = DurationSerializer()
    genres = GenreSerializer(many=True)
    directors = PersonSerializer(many=True)
    actors = PersonSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'score', 'year', 'synopsis', 'cover', 'duration',
                  'genres', 'directors', 'actors']
