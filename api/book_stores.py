import requests
from django.conf import settings
from django.utils.module_loading import import_string
from requests import ConnectionError

from api.api_utils import get_response_status_info
from api.serializers import IceAndFireSerializer


class BookStore(object):
    """
    Books store class which encapsulate all store specific information with itself.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the store from the active store settings.
        """
        store_class = import_string(settings.ACTIVE_BOOK_STORE)
        self.store = store_class(*args, **kwargs)

    def get_books(self, name):
        """Fetch the books from the active store."""
        return self.store.get_books(name)


class BookStoreBase(object):
    """Base class for all stores to have common attributes and functions."""
    pass


class IceAndFireStore(BookStoreBase):
    url = 'https://www.anapioficeandfire.com/api/books'
    serializer = IceAndFireSerializer

    def parse_query_params(self, name):
        """Helper method which parses the query string and construct api url."""
        if not name:
            return self.url
        return '{0}?name={1}'.format(self.url, name)

    def get_books(self, name=None):
        """Fetch the books information using the api url."""
        api_url = self.parse_query_params(name)
        try:
            response = requests.get(api_url)
            return self.transform_response(response)
        except ConnectionError as ex:
            return self.return_error_response(ex)

    def transform_response(self, response):
        """Transforms the response into required format"""
        response_data = response.json()
        serialized_data = []
        for book_data in response_data:
            serializer = self.serializer(book_data)
            serialized_data.append(serializer.data)

        response_status = get_response_status_info(response.status_code)
        data = {'data': serialized_data}
        data.update(response_status)
        return data

    def return_error_response(self, ex):
        """Returns error response."""
        response_status = get_response_status_info(status_code=500)
        response_status['message'] = '{error}'.format(error=ex.message)
        return response_status
