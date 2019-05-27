from rest_framework.test import APITestCase

from api.serializers import BookSerializer, MinimalBookSerializer
from api.tests.factories import BookFactory


class BookSerializerTests(APITestCase):
    def setUp(self):
        super(BookSerializerTests, self).setUp()
        self.book = BookFactory()

    def test_book_serializer(self):
        """Test book serializer has all the required fields"""
        serializer = BookSerializer(instance=self.book)
        for field in serializer.fields:
            self.assertIsNotNone(serializer.data.get(field))

    def test_book_minimal_serializer(self):
        """Test minimal book serializer has all the required fields but the excluded"""
        serializer = MinimalBookSerializer(instance=self.book)
        excluded_fields = serializer.Meta.exclude
        for field in excluded_fields:
            self.assertNotIn(field, serializer.data)
