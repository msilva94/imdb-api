from movies.models import Movie, Person, Genre
from rest_framework import serializers


class DurationSerializer(serializers.Serializer):
    hours = serializers.IntegerField(source='hour')
    minutes = serializers.IntegerField(source='minute')

    class Meta:
        fields = ['hours' ,'minutes']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id', 'title']


class MovieListSerializer(MovieBaseSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='movie-detail')

    class Meta(MovieBaseSerializer.Meta):
        fields = MovieBaseSerializer.Meta.fields + [
            'score', 'year', 'cover', 'url']


class PersonListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='person-detail')

    class Meta:
        model = Person
        fields = ['id', 'name', 'url']


class MovieSerializer(MovieBaseSerializer):
    duration = DurationSerializer()
    genres = GenreSerializer(many=True)
    directors = PersonListSerializer(many=True)
    actors = PersonListSerializer(many=True)

    class Meta(MovieBaseSerializer.Meta):
        fields = MovieBaseSerializer.Meta.fields + [
            'score', 'year', 'synopsis', 'cover', 'duration', 'genres', 'directors', 'actors']


class PersonSerializer(serializers.ModelSerializer):
    movies = MovieBaseSerializer(many=True)

    class Meta:
        model = Person
        fields = ['id', 'name', 'movies']
