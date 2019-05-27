from dateutil import parser
from rest_framework import serializers

from api.models import Author, Book, Country, ExternalBook, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)

    def to_representation(self, instance):
        return instance.name

    def to_internal_value(self, data):
        instance, __ = Author.objects.get_or_create(name=data)
        return instance


class CountryField(serializers.Field):
    def to_representation(self, country):
        return country.name

    def to_internal_value(self, data):
        try:
            return Country.objects.get(name=data)
        except Country.DoesNotExist as ex:
            raise serializers.ValidationError(u"Country {} does not exist.".format(data))


class PublisherField(serializers.Field):
    def to_internal_value(self, data):
        try:
            return Publisher.objects.get(name=data)
        except Publisher.DoesNotExist:
            raise serializers.ValidationError(u"Publisher {} does not exist.".format(data))

    def to_representation(self, publisher):
        return publisher.name


class BookSerializer(serializers.ModelSerializer):
    """Book serializer with all fields"""
    authors = AuthorSerializer(many=True)
    country = CountryField()
    publisher = PublisherField()

    class Meta:
        model = Book
        fields = ('id', 'name', 'isbn', 'authors', 'number_of_pages', 'publisher', 'country', 'release_date')

    def create(self, validated_data):
        """Overriding create method to write nested relationships"""
        authors = validated_data.pop('authors', None)

        book = super(BookSerializer, self).create(validated_data)
        book.authors.add(*authors)
        return book

    def update(self, instance, validated_data):
        """Overriding update method to write nested relationships"""
        authors = validated_data.pop('authors', None)
        book = super(BookSerializer, self).update(instance, validated_data)
        self._update_authors(instance, authors)
        return book

    def _update_authors(self, instance, validated_authors):
        """Helper method to update book authors"""
        if validated_authors is None:
            return
        instance.authors.clear()
        instance.authors.add(*validated_authors)


class MinimalBookSerializer(BookSerializer):
    """
    Use this serializer where all the model fields are not required.
    """

    class Meta:
        model = Book
        exclude = ('id',)


class ExternalAuthorSerializer(serializers.Serializer):
    """Author Serializer for external api"""

    def to_representation(self, instance):
        return instance


class ExternalDateField(serializers.DateField):
    """Custom date field to handle external api date."""

    def to_representation(self, value):
        parsed_date = parser.parse(value).date()
        return super(ExternalDateField, self).to_representation(parsed_date)


class IceAndFireSerializer(serializers.Serializer):
    """
    Serializer for transforming external api data.
    """

    def __init__(self, data=None, *args, **kwargs):
        """
        Initializes an external book object with data and passes the instance to
        super class.
        """
        external_book = ExternalBook(**data)
        super(IceAndFireSerializer, self).__init__(external_book, *args, **kwargs)

    name = serializers.CharField()
    isbn = serializers.CharField()
    authors = ExternalAuthorSerializer(many=True)
    number_of_pages = serializers.IntegerField(source='numberOfPages')
    publisher = serializers.CharField()
    country = serializers.CharField()
    release_date = ExternalDateField(format="%Y-%m-%d", source='released')
