from django.contrib import admin, messages
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.urls import reverse
from utils.admin import ViewOnlyAdminMixin

from .forms import ImportMovieForm
from .models import Genre, ImportMovie, Movie, Person


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'score', 'year')
    search_fields = ('title',)
    autocomplete_fields = ('genres', 'directors', 'actors',)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(ImportMovie)
class ImportMovieAdmin(ViewOnlyAdminMixin, admin.ModelAdmin):
    change_list_template = 'movies/import_movie_form.html'

    def changelist_view(self, request, extra_context=None):
        response = super(ImportMovieAdmin, self).changelist_view(request, extra_context)

        if request.method == 'POST':
            form = ImportMovieForm(request.POST)

            if form.is_valid():
                external_id = form.cleaned_data['external_id']
                title = call_command('import_movie', id=external_id)
                messages.add_message(request, messages.INFO, f'Imported movie: {title}')
                return HttpResponseRedirect(reverse('admin:index'))

        else:
            print('init form')
            form = ImportMovieForm()

        extra_context = {
            'form': form,
            'title': 'Importa Movie'
        }
        response.context_data.update(extra_context)
        return response
