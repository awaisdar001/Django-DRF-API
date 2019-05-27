from api.book_stores import BookStore


class BooksService(object):
    """Books service for fetching books related information from the api."""

    def get_books(self, name=None):
        """Returns & transforms the books information."""
        return BookStore().get_books(name)
