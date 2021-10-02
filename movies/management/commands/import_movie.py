import re
from datetime import time

import urllib3
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from movies.models import Genre, Movie, Person

IMDB_BASE_URL = 'https://imdb.com'
IMDB_MOVIE_URL = f'{IMDB_BASE_URL}/title/'


class Command(BaseCommand):
    help = 'Import movie from IMDb'

    def add_arguments(self, parser):
        parser.add_argument(
            '--id',
            type=str,
            required=True,
            help='IMDb ID',
        )

    def handle(self, *args, **options):
        external_id = options.get('id')

        if not re.match('tt\d+', external_id):
            raise CommandError('Invalid IMDb ID')

        try:
            return Movie.objects.get(external_id=external_id).title
        except Movie.DoesNotExist:
            pass

        movie_url = f'{IMDB_MOVIE_URL}{external_id}/'

        request = self.get_page(movie_url)
        if not request.status == 200:
            raise CommandError('Movie not found')

        soup = BeautifulSoup(request.data, 'html.parser')

        header_section = soup.find('section', class_='ipc-page-section')
        title = header_section.find('h1').get_text()
        year_duration_wrapper = header_section.find('ul').find_all('li')
        year, duration = year_duration_wrapper[0].find('a').get_text(), self.get_duration(year_duration_wrapper[2].get_text())
        score = header_section.find('div', class_='ipc-button__text').find('span').get_text()
        synopsis = soup.find('span', class_='gCtawA').get_text()
        genres = [genre.get_text() for genre in soup.find('div', class_='gtBDBL').find_all('a')]

        persons_wrapper = soup.find('ul', class_='ipc-metadata-list').find_all('li', class_='ipc-metadata-list__item')
        directors = [(director.get_text(), self.get_person_id(director['href'])) for director in persons_wrapper[0].find_all('a') if not 'full' in director['href']]
        actors = [(actor.get_text(), self.get_person_id(actor['href'])) for actor in persons_wrapper[2].find_all('a') if not 'full' in actor['href']]

        cover_url = f"{IMDB_BASE_URL}{soup.find('a', class_='ipc-lockup-overlay')['href']}"
        request = self.get_page(cover_url)
        soup = BeautifulSoup(request.data, 'html.parser')
        cover = soup.find('img', class_='bnaOri')['src']

        movie, _ = Movie.objects.get_or_create(
            external_id=external_id,
            defaults={
                'title': title,
                'year': year,
                'score': score,
                'synopsis': synopsis,
                'duration': duration,
                'cover': cover,
            }
        )

        for g in genres:
            genre, _ = Genre.objects.get_or_create(
                name=g,
            )
            movie.genres.add(genre)

        for d, external_id in directors:
            director, _ = Person.objects.get_or_create(
                external_id=external_id,
                defaults={
                    'name': d,
                }
            )
            movie.directors.add(director)

        for a, external_id in actors:
            actor, _ = Person.objects.get_or_create(
                external_id=external_id,
                defaults={
                    'name': a,
                }
            )
            movie.actors.add(actor)

        return title

    def get_title_year(self, title):
        year = None
        year_regex = '\((\d{4})\)'
        year_search = re.search(year_regex, title)

        if year_search:
            year = year_search.group(1)
            title = re.sub(year_regex, '', title).strip()

        return title, year

    def get_duration(self, duration):
        duration = re.match('((?P<hour>\d+)h)?\s?((?P<minutes>\d+)min)?', duration)
        hour, minutes = duration.group('hour'), duration.group('minutes')
        hour = int(hour) if hour else 0
        minutes = int(minutes) if minutes else 0

        return time(hour, minutes)

    def get_person_id(self, person):
        return re.search('nm\d+', person).group(0)

    def get_page(self, url):
        http = urllib3.PoolManager()
        request = http.request(
            'GET',
            url,
            headers={
                'Accept-Language': 'en-US,en',
            }
        )
        return request
