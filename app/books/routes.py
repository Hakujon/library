from fastapi import APIRouter
from sqlalchemy import select

from app.books.models import Book, Author
from app.books.schemas import BookResponse, BookCreate
from app.books.schemas import AuthorCreate, AuthorResponse
from app.database import DB_SESSION


router_books = APIRouter(prefix="/books", tags=["Работа с книгами"])


@router_books.get("/", response_model=list[BookResponse])
async def get_all_books(db_session: DB_SESSION):
    query = select(Book)
    result = await db_session.execute(query)
    books = result.scalars().all()
    return [BookResponse.model_validate(book) for book in books]


@router_books.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id(book_id: int, db_session: DB_SESSION):
    query = select(Book).filter(Book.id == book_id)
    result = await db_session.execute(query)
    book = result.scalars().first()
    return BookResponse.model_validate(book)


@router_books.post("/")
async def create_book(book: BookCreate, db_session: DB_SESSION):
    book_to_db = Book(**book.model_dump())
    db_session.add(book_to_db)
    await db_session.commit()
    await db_session.refresh(book_to_db)
    return {
        "message": "Book was added!",
        "book": BookResponse.model_validate(book_to_db)
    }


@router_books.get("/authors", response_model=list[AuthorResponse])
async def get_all_authors(db_session: DB_SESSION):
    query = select(Author)
    result = await db_session.execute(query)
    authors = result.scalars().all()
    return [AuthorResponse.model_validate(author) for author in authors]


@router_books.get("/authors/{author_id}")
async def get_author_by_id(author_id: int, db_session: DB_SESSION):
    query = select(Author).filter(Author.id == author_id)
    result = await db_session.execute(query)
    author = result.scalars().first()
    return AuthorResponse.model_validate(author)


@router_books.post("/authors")
async def create_author(author: AuthorCreate, db_session: DB_SESSION):
    author_to_db = Author(**author.model_dump())
    db_session.add(author_to_db)
    await db_session.commit()
    await db_session.refresh(author_to_db)
    return {
        "message": "Author was created",
        "author": AuthorResponse.model_validate(author_to_db)
    }
