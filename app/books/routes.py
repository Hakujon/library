from fastapi import APIRouter
from sqlalchemy import select

from app.books.models import Book
from app.books.schemas import BookBase, BookResponse
from app.database import DB_SESSION


router_books = APIRouter(prefix="/books", tags=["Работа с книгами"])


@router_books.get("/")
async def get_all_books(db_session: DB_SESSION):
    query = select(Book)
    result = await db_session.execute(query)
    books = result.scalars().all()
    return [BookResponse.model_validate(book) for book in books]


@router_books.get("/{book_id}")
async def get_book_by_id(book_id: int, db_session: DB_SESSION):
    query = select(Book).filter(Book.id == book_id)
    result = await db_session.execute(query)
    book = result.scalars().first()
    return BookResponse.model_validate(book)


@router_books.post("/")
async def create_book(book: BookBase, db_session: DB_SESSION):
    book_to_db = Book(**book.model_dump())
    db_session.add(book_to_db)
    await db_session.commit()
    await db_session.refresh(book_to_db)
    return {
        "message": "Book was added!",
        "book": BookResponse.model_validate(book_to_db)
    }
