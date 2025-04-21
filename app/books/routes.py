from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.books.models import Book
from app.books.schemas import BookBase
from database import get_db, DB_SESSION


router = APIRouter(prefix="/books", tags=["Работа с книгами"])

@router.get("/")
async def get_all_books(db_session: DB_SESSION):
    query = select(Book)
    result = await db_session.execute(query)
    books = result.scalars().all()
    return books


@router.get("/{book_id}")
async def get_book_by_id(book_id: int, db_session: DB_SESSION):
    query = select(Book).filter(Book.id==book_id)
    result = await db_session.execute(query)
    book = result.scalars().first()
    return book


@router.post("/")
async def create_book(book: BookBase, db_session: DB_SESSION):
