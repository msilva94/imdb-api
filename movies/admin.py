from django.contrib import admin

from .models import Genre, Movie, Person


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'score', 'year')
    search_fields = ('title',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass
