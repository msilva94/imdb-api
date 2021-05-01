import re
from datetime import time

import urllib3
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from movies.models import Genre, Movie, Person

IMDB_BASE_URL = 'https://imdb.com/'
IMDB_MOVIE_URL = f'{IMDB_BASE_URL}title/'


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

        http = urllib3.PoolManager()
        request = http.request(
            'GET',
            movie_url,
            headers={
                'Accept-Language': 'en-US,en',
            }
        )

        if not request.status == 200:
            raise CommandError('Movie not found')

        soup = BeautifulSoup(request.data, 'html.parser')

        title_wrapper = soup.find('div', class_='title_wrapper')
        subtext = title_wrapper.find('div', class_='subtext')
        summary_items = soup.find_all('div', class_='credit_summary_item')

        title, year = self.get_title_year(title_wrapper.find('h1').get_text())
        score = soup.find('span', itemprop='ratingValue').get_text()
        synopsis = soup.find('div', class_='summary_text').get_text().strip()
        duration = self.get_duration(subtext.find('time').get_text().strip())
        genres = [genre.get_text() for genre in subtext.find_all('a')][:-1]
        cover = soup.find('div', class_='poster').find('img')['src']
        directors = [(director.get_text(), self.get_person_id(director['href'])) for director in summary_items[0].find_all('a')]
        actors = [(actor.get_text(), self.get_person_id(actor['href'])) for actor in summary_items[2].find_all('a')[:-1]]

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
        duration = re.match('((?P<hour>\d+)h)?\s?(?P<minutes>\d+)min', duration)
        hour, minutes = duration.group('hour'), int(duration.group('minutes'))
        hour = int(hour) if hour else 0

        return time(hour, minutes)

    def get_person_id(self, person):
        return re.search('nm\d+', person).group(0)