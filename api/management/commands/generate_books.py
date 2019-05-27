# -*- coding: utf-8 -*-

import random
import uuid
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand, CommandError

from api.models import Author, Book, Country, Publisher


class Command(BaseCommand):
    """
    This command will generate batch of books with random data for testing.

    By running this command, books with random data will be generated.
    The data selection is done at the random to ensure that books will have
    distinct data, which will provide help for filtering.

    EXAMPLE USAGE:
        ./manage.py generate_books --batch_size=100
    OR
        ./manage.py generate_books

    If batch size is not provided, the command will generate 10 books

    """

    help = "Populate books model with random data"

    def add_arguments(self, parser):
        """
        Defining the arguments to be used by the command.
        """
        parser.add_argument(
            '--batch_size',
            type=int,
            default=10,
            dest='batch_size',
            help="number to books to generate"
        )

    @staticmethod
    def get_random_publisher():
        """Get a random publisher instance"""
        publishers = ['DestinationPakistan', 'Traverse', 'IBNFreaks']
        publisher, __ = Publisher.objects.get_or_create(name=random.choice(publishers))
        return publisher

    @staticmethod
    def get_random_country():
        """Get a random country instance"""
        country_names = [
            'Pakistan', 'United States', 'Morocco', 'Turkey', 'United Kingdom',
            'Australia', 'New Zealand'
        ]
        country, __ = Country.objects.get_or_create(name=random.choice(country_names))
        return country

    @staticmethod
    def get_random_authors():
        """Get random list of authors from some pre-defined authors set"""
        authors = ['Awais Jibran', 'Adeva', 'A.R. Akram', 'Rehman G']
        author_instances = []
        for author in random.sample(authors, random.choice(range(0, 3))):
            author, __ = Author.objects.get_or_create(name=author)
            author_instances.append(author)
        return author_instances

    @staticmethod
    def get_random_release_date():
        """Get random book release date in the past"""
        relative_month = random.choice(range(-36, 36))
        return datetime.now() + relativedelta(months=relative_month)

    def handle(self, *args, **options):
        """
        Generate books based on the input.
        """
        batch_size = options['batch_size']
        for count in range(0, batch_size):
            book = Book(
                name="Book: {}".format(count),
                isbn='BNF-{}'.format(uuid.uuid4()),
                country=self.get_random_country(),
                publisher=self.get_random_publisher(),
                number_of_pages=random.choice(range(100, 1000)),
                release_date=self.get_random_release_date()
            )

            try:
                book.save()
            except Exception as e:
                raise CommandError(self.stderr.write(
                    'Error Saving Book {}\n{}'.format(book.id, e)))

            book.authors = self.get_random_authors()
            book.save()

            self.stdout.write(self.style.SUCCESS('Book ID Created: %s') % book.id)
