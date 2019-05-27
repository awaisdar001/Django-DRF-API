from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.api_utils import get_response_status_info
from api.filters import BookFilter
from api.models import Book
from api.serializers import BookSerializer, MinimalBookSerializer


class BookViewSet(ModelViewSet):
    """View set for CURD operation on book model"""
    queryset = Book.objects.all()
    lookup_field = 'id'
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BookFilter

    def get_serializer_class(self):
        """Return the class to use for the serializer."""
        if self.action == 'create':
            return MinimalBookSerializer
        return BookSerializer

    def list(self, request, *args, **kwargs):
        """List the books queryset"""
        response = super(BookViewSet, self).list(request, *args, **kwargs)
        response_data = self.transform_response_for_list(response)
        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        """Retrieves a single book using book-id"""
        response = super(BookViewSet, self).retrieve(request, *args, **kwargs)
        response_data = self.transform_response_for_retrieve(response)
        return Response(response_data)

    def create(self, request, *args, **kwargs):
        """View for creating a book instance"""
        response = super(BookViewSet, self).create(request, *args, **kwargs)
        response_data = self.transform_data_for_create(response)
        return Response(response_data)

    def update(self, request, *args, **kwargs):
        """View for updating a book instance"""
        response = super(BookViewSet, self).update(request, *args, **kwargs)
        book = self.get_object()
        response_data = self.transform_data_for_update(response, book)

        return Response(data=response_data)

    def destroy(self, request, *args, **kwargs):
        """View for deleting a book instance from the model."""
        book = self.get_object()
        response = super(BookViewSet, self).destroy(request, *args, **kwargs)
        response_data = self.transform_response_for_destroy(response, book)
        return Response(data=response_data)

    @staticmethod
    def transform_response(data, status_code):
        response_status = get_response_status_info(status_code)
        data.update(response_status)

    def transform_response_for_list(self, response):
        response_data = {
            'data': response.data
        }
        self.transform_response(response_data, response.status_code)
        return response_data

    def transform_response_for_retrieve(self, response):
        response_data = {
            'data': response.data
        }
        self.transform_response(response_data, response.status_code)
        return response_data

    def transform_data_for_create(self, response):
        response_data = {
            'data': {'book': response.data}
        }
        self.transform_response(response_data, response.status_code)
        return response_data

    def transform_data_for_update(self, response, book):
        response_data = {
            'data': response.data,
            'message': 'The book {0} was updated successfully'.format(book.name),
        }
        self.transform_response(response_data, response.status_code)
        return response_data

    def transform_response_for_destroy(self, response, book):
        response_data = {
            'data': [],
            'message': 'The book {0} was deleted successfully'.format(book.name)
        }
        self.transform_response(response_data, response.status_code)
        return response_data
