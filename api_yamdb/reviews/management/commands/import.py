import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, Review,  # isort:skip
                            Title)
from users.models import User  # isort:skip


class Command(BaseCommand):
    help = 'Command to import data from csv-files into database.'
    DATA_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../../static/data/'))

    FILE_NAMES = [
        'users',
        'category',
        'genre',
        'titles',
        'genre_title',
        'review',
        'comments',
    ]

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='specific filename '
                            'or "all" to import all files at once')

    def create_users_object(self, row):
        User.objects.create(
            pk=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name'],
        )

    def create_category_object(self, row):
        Category.objects.create(
            pk=row['id'],
            name=row['name'],
            slug=row['slug'],
        )

    def create_genre_object(self, row):
        Genre.objects.create(
            pk=row['id'],
            name=row['name'],
            slug=row['slug'],
        )

    def create_titles_object(self, row):
        Title.objects.create(
            pk=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(pk=row['category'])
        )

    def create_genre_title_object(self, row):
        title = Title.objects.get(
            pk=row['title_id'],
        )
        title.genre.add(Genre.objects.get(pk=row['genre_id']))
        title.save()

    def create_review_object(self, row):
        Review.objects.create(
            pk=row['id'],
            title=Title.objects.get(pk=row['title_id']),
            text=row['text'],
            author=User.objects.get(pk=row['author']),
            score=row['score'],
            pub_date=row['pub_date'],
        )

    def create_comments_object(self, row):
        Comment.objects.create(
            pk=row['id'],
            review=Review.objects.get(pk=row['review_id']),
            text=row['text'],
            author=User.objects.get(pk=row['author']),
            pub_date=row['pub_date'],
        )

    def import_file(self, file_name):
        try:
            with open(Command.DATA_DIR + f'\\{file_name}.csv',
                      encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.__getattribute__(f'create_{file_name}_object')(row)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error to import: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Data from {file_name} imported to db!'
            ))

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']

        if filename == 'all':
            for file_name in self.FILE_NAMES:
                self.import_file(file_name)
        else:
            self.import_file(filename)
