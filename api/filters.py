from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from api.models import Book


class BookFilter(FilterSet):
    """Custom filter which provides data filtration per field for book model."""

    release_date = NumberFilter(field_name='release_date', lookup_expr='year')
    publisher = CharFilter(field_name='publisher', lookup_expr='name')

    class Meta:
        model = Book
        fields = ['name', 'isbn']
