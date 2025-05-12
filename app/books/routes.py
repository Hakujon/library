from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.books.models import Book, Author
from app.books.schemas import BookResponse, BookCreate
from app.books.schemas import AuthorCreate, AuthorResponse
from app.database import DB_SESSION

from app.books.dao import BookDAO, AuthorDAO
from app.books.rb import RBBook, RBAuthor


router_books = APIRouter(prefix="/books", tags=["Работа с книгами"])


@router_books.get("/")
async def get_all_books(
    request_body: Annotated[RBBook, Depends()],
    db_session: DB_SESSION
        ) -> list[BookResponse] | dict:
    books = await BookDAO.find_all(db_session, **request_body.to_dict())
    if not books:
        return {"message": "books not found"}
    return [BookResponse.model_validate(book) for book in books]


@router_books.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id(
    book_id: int,
    db_session: DB_SESSION
        ) -> BookResponse | dict:
    book = await BookDAO.find_one_by_id(db_session, book_id)
    if book is None:
        return {"message": f"Book with {book_id} not found"}
    return BookResponse.model_validate(book)


@router_books.post("/", response_model=BookResponse)
async def create_book(book: BookCreate, db_session: DB_SESSION):
    book_to_db = await BookDAO.add(db_session, **book.model_dump())
    return {
        "message": "Book was added!",
        "book": BookResponse.model_validate(book_to_db)
    }


@router_books.patch("/{book_id}")
async def rework_book(
    book_id: int,
    new_book: BookCreate,
    db_session: DB_SESSION
        ):

    book_to_rework = await BookDAO.find_one_by_id(db_session, book_id)
    updated_data_dict = new_book.model_dump()
    for key, value in updated_data_dict.items():
        setattr(book_to_rework, key, value)

    await db_session.commit()
    await db_session.refresh(book_to_rework)
    return {
        "message": f"Book {book_id} was changed",
        "book": BookResponse.model_validate(book_to_rework)
    }


@router_books.get("/authors", response_model=list[AuthorResponse])
async def get_all_authors(
    request_body: Annotated[RBAuthor, Depends()],
    db_session: DB_SESSION,
        ) -> list[AuthorResponse] | dict:
    authors = await AuthorDAO.find_all(
        session=db_session, **request_body.to_dict()
        )
    if not authors:
        return {"message": "Authors not found"}
    return [AuthorResponse.model_validate(author) for author in authors]


@router_books.get("/authors/{author_id}", response_model=AuthorResponse)
async def get_author_by_id(
    author_id: int, db_session: DB_SESSION
        ) -> AuthorResponse | dict:
    author = await AuthorDAO.find_one_by_id(
        session=db_session, data_id=author_id)
    return AuthorResponse.model_validate(author)


@router_books.post("/authors")
async def create_author(author: AuthorCreate, db_session: DB_SESSION):
    author_to_db = await AuthorDAO.add(
        session=db_session,
        **author.model_dump()
    )
    return {
        "message": "Author was created",
        "author": AuthorResponse.model_validate(author_to_db)
    }
