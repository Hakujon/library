from app.dao.base import BaseDAO
from app.books.models import Book, Author


class BookDAO(BaseDAO):
    model = Book


class AuthorDAO(BaseDAO):
    model = Author
