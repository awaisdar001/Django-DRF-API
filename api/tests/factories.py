import datetime

import factory
from factory.fuzzy import FuzzyDate, FuzzyInteger, FuzzyText

from api.models import Author, Book, Country, Publisher


class CountryFactory(factory.DjangoModelFactory):
    name = FuzzyText()

    class Meta:
        model = Country


class AuthorFactory(factory.DjangoModelFactory):
    name = FuzzyText()

    class Meta:
        model = Author


class PublisherFactory(factory.DjangoModelFactory):
    name = FuzzyText()

    class Meta:
        model = Publisher


class BookFactory(factory.DjangoModelFactory):
    name = FuzzyText()
    isbn = factory.Sequence(lambda n: 'isbn_%d' % n)
    country = factory.SubFactory(CountryFactory)
    number_of_pages = FuzzyInteger(10, 650)
    release_date = FuzzyDate(datetime.date(2008, 1, 1))
    publisher = factory.SubFactory(PublisherFactory)

    class Meta:
        model = Book

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        """The post_generation decorator performs actions once the model object has been generated."""
        if not extracted:
            extracted = ['George R. R. Martin']
        for author in extracted:
            self.authors.add(AuthorFactory.simple_generate(create, name=author))
