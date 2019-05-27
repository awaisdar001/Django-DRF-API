import mock
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.tests.factories import BookFactory, CountryFactory, PublisherFactory

MockedEmptyResponse = mock.Mock(status_code=200, json=mock.Mock(return_value=[]))
MockResponse = mock.Mock(
    status_code=200,
    json=mock.Mock(
        return_value=[{
            'url': 'dummy-url',
            'name': 'dummy-name',
            'isbn': '90-12',
            'authors': ['George R. R. Martin'],
            'numberOfPages': 90,
            'publisher': 'Batam Pages',
            'country': 'United States',
            'characters': [],
            'released': '1996-08-01T00:00:00'
        }]
    )
)


class BooksTests(APITestCase):
    books_api_url = reverse('api:v1:books-list')

    def setUp(self):
        """Setup some data for testing"""
        super(BooksTests, self).setUp()
        morocco_publisher = PublisherFactory(name='Morocco Books')
        lahore_publisher = PublisherFactory(name='Lahore Books')
        usa_publisher = PublisherFactory(name='USA Books')
        self.book1 = BookFactory(
            name='Book 1',
            isbn='M-Book1',
            publisher=morocco_publisher,
            release_date='2018-01-01',
        )
        self.book2 = BookFactory(
            name='Book 2',
            isbn='L-Book2',
            publisher=lahore_publisher,
            release_date='2019-01-01',
        )
        self.book3 = BookFactory(
            name='Book 3',
            isbn='U-Book3',
            publisher=usa_publisher,
            release_date='2020-01-01',
        )

    def assert_book1_data(self, response_data):
        self.assert_response_success(response_data)
        book = response_data['data'][0]
        self.assertEqual(book['name'], 'Book 1')
        self.assertEqual(book['isbn'], 'M-Book1')
        self.assertEqual(book['publisher'], 'Morocco Books')
        self.assertEqual(book['release_date'], '2018-01-01')

    def assert_book2_data(self, response_data):
        self.assert_response_success(response_data)
        book = response_data['data'][0]
        self.assertEqual(book['name'], 'Book 2')
        self.assertEqual(book['isbn'], 'L-Book2')
        self.assertEqual(book['publisher'], 'Lahore Books')
        self.assertEqual(book['release_date'], '2019-01-01')

    def assert_book3_data(self, response_data):
        self.assert_response_success(response_data)
        book = response_data['data'][0]
        self.assertEqual(book['name'], 'Book 3')
        self.assertEqual(book['isbn'], 'U-Book3')
        self.assertEqual(book['publisher'], 'USA Books')
        self.assertEqual(book['release_date'], '2020-01-01')

    def book_detail_url(self, _id):
        """Returns book details url."""
        return '{}{}/'.format(self.books_api_url, _id)

    def book_search_url(self, data):
        """Construct api search url based on key value data."""
        query_string_params = ['{0}={1}'.format(key, value) for key, value in data.items()]
        query_string = '&'.join(query_string_params)
        return '{0}?{1}'.format(self.books_api_url, query_string)

    def make_api_get_request(self, url, data=None):
        response = self.client.get(url, data=data)
        return response.json()

    def assert_response_success(self, response_data):
        """Helper method to verify if the response was successful"""
        self.assertEqual(response_data.get('status_code'), 200)
        self.assertEqual(response_data.get('status'), 'success')

    def assert_response_data_count(self, response, expected_count):
        self.assertEqual(len(response['data']), expected_count)


class BooksCRUDTests(BooksTests):
    """Tests for crud operations on Book viewset"""

    def __init__(self, *args, **kwargs):
        super(BooksCRUDTests, self).__init__(*args, **kwargs)

    def test_api_books_list_response_status(self):
        """Tests that successful response contains response status information."""
        response_data = self.make_api_get_request(self.books_api_url)
        self.assert_response_success(response_data)

    def test_api_books_list_data(self):
        """Tests that successful response contains response status information."""
        response_data = self.make_api_get_request(self.books_api_url)
        self.assert_response_success(response_data)
        self.assert_response_data_count(response_data, 3)

    def test_book_retrieve(self):
        """Tests that retrieve end point returns expected data"""
        response_data = self.make_api_get_request(self.book_detail_url(self.book1.id))
        self.assert_response_success(response_data)
        self.assertIsNotNone(response_data.get('data'))
        self.assertEqual(response_data['data']['name'], 'Book 1')

    def test_book_update(self):
        """Tests that patch endpoint updates the data correctly."""
        new_book_name = 'Updated book name'
        book_detail_url = self.book_detail_url(self.book1.id)
        response = self.client.patch(book_detail_url, data={'name': new_book_name}, format='json')
        response_data = response.json()

        self.assert_response_success(response_data)
        self.assertIn('message', response_data)
        self.assertEqual(
            response_data['message'],
            'The book {} was updated successfully'.format(new_book_name)
        )

    def test_book_destroy(self):
        """Tests that delete operation works accordingly."""
        book_name = self.book1.name
        book_detail_url = self.book_detail_url(self.book1.id)
        response = self.client.delete(book_detail_url)
        response_data = response.json()

        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'The book {} was deleted successfully'.format(book_name))
        self.assertEqual(response_data['data'], [])

    def test_book_create(self):
        """Tests that book create endpoint successfully adds a new book"""
        country = CountryFactory()
        publisher = PublisherFactory()
        data = {
            'name': 'My New Book',
            'isbn': 'isbn-9989',
            'authors': ['Awais Jibran'],
            'country': country.name,
            'number_of_pages': 32,
            'publisher': publisher.name,
            'release_date': '2019-05-19'
        }
        response_data = self.make_api_get_request(self.books_api_url)
        pre_create_book_count = len(response_data['data'])

        response = self.client.post(self.books_api_url, data=data, format='json')
        response_data = response.json()
        self.assertEqual(response_data['data'], {'book': data})

        response_data = self.make_api_get_request(self.books_api_url)
        post_create_book_count = len(response_data['data'])

        self.assertGreater(post_create_book_count, pre_create_book_count)
        self.assertEqual(post_create_book_count, pre_create_book_count + 1)


class FilterBookTests(BooksTests):
    """Tests for book filter"""

    def setUp(self):
        super(FilterBookTests, self).setUp()

    def test_filter_by_name(self):
        """Tests that filter by name returns expected data."""
        response_data = self.make_api_get_request(self.books_api_url)
        self.assert_response_data_count(response_data, 3)
        book_search_url = self.book_search_url({'name': 'Book 1'})
        response_data = self.make_api_get_request(book_search_url)
        self.assert_response_data_count(response_data, 1)
        self.assert_book1_data(response_data)

    def test_filter_by_publisher(self):
        """Tests that filter by publisher name returns expected data."""
        book_search_url = self.book_search_url({'publisher': 'Lahore Books'})
        response_data = self.make_api_get_request(book_search_url)
        self.assert_response_data_count(response_data, 1)
        self.assert_book2_data(response_data)

    def test_filter_by_isbn(self):
        """Tests that filter by isbn returns expected data."""
        book_search_url = self.book_search_url({'isbn': 'U-Book3'})
        response_data = self.make_api_get_request(book_search_url)
        self.assert_response_data_count(response_data, 1)
        self.assert_book3_data(response_data)

    def test_filter_by_release_date(self):
        """Tests that filter by release date returns expected data."""
        book_search_url = self.book_search_url({'release_date': '2018'})
        response_data = self.make_api_get_request(book_search_url)
        self.assert_response_data_count(response_data, 1)
        self.assert_book1_data(response_data)

    def test_filter_combined(self):
        """Tests that we can combine the filter fields and get expected data."""
        book_search_url = self.book_search_url({
            'name': 'Book 1',
            'isbn': 'M-Book1',
            'publisher': 'Morocco Books',
            'release_date': '2018',
        })
        response_data = self.make_api_get_request(book_search_url)
        self.assert_response_data_count(response_data, 1)
        self.assert_book1_data(response_data)
