from django.contrib import admin

from .models import Genre, Movie, Person


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
