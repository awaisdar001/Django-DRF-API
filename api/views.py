from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from api.services import BooksService


class BooksList(APIView):
    """Get the books data from external api"""
    book_service = BooksService()

    def get(self, request):
        """
        Returns the all books information or filtered books based on
        query param.
        """
        query_params = request.query_params
        response_data = self.book_service.get_books(name=query_params.get('name'))
        return Response(response_data, status=HTTP_200_OK)
