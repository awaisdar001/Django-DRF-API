import mock
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

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


class BooksListTests(APITestCase):
    books_fetch_url = reverse('api:external_books')

    @mock.patch('requests.get', return_value=MockResponse)
    def test_api_response_transformation(self, __):
        """Tests that the data is correctly transformed into the required
        format."""
        response = self.client.get(self.books_fetch_url)
        response_data = response.json()
        self.assertGreaterEqual(len(response_data['data']), 1)

        book_1 = response_data['data'][0]
        self.assertIn('number_of_pages', response_data['data'][0], book_1)
        self.assertIn('release_date', response_data['data'][0], book_1)
        self.assertEqual(book_1['release_date'], '1996-08-01')

    @mock.patch('requests.get', return_value=MockResponse)
    def test_api_response_with_extra_fields(self, __):
        """
        Tests that the data is extra fields are removed and not included in
        output.
        """
        response = self.client.get(self.books_fetch_url)
        response_data = response.json()
        book_1 = response_data['data'][0]
        self.assertNotIn('characters', book_1)
        self.assertNotIn('url', book_1)

    @mock.patch('requests.get', return_value=MockedEmptyResponse)
    def test_empty_get_books(self, __):
        """ Tests that empty response contains response status information. """
        response = self.client.get(self.books_fetch_url)
        response_data = response.json()
        self.assertIn('data', response_data)
        self.assertEqual(response_data['data'], [])
        self.assertIn('status', response_data)
        self.assertEqual(response_data['status'], 'success')

    @mock.patch('requests.get', return_value=MockedEmptyResponse)
    def test_call_with_querystring(self, mocked_api_call):
        """
        Test api call contains querystring when user provides the filter
        criteria in querystring
        """
        filter_name = 'Foo'
        __ = self.client.get(self.books_fetch_url, {'name': filter_name})
        self.assertEqual(
            mocked_api_call.call_args[0][0],
            'https://www.anapioficeandfire.com/api/books?name={}'.format(filter_name))
