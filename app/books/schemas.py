from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class BookBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(..., description="Название книги")
    description: Optional[str] = Field(
        None, max_length=500, description="Описание книги"
    )
    date_publication: date = Field(..., description="Дата публикации книги")
    author_id: int = Field(..., ge=1, description="ID автора книги")


class AuthorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: str = Field(..., description="Имя автора")
    last_name: str = Field(..., description="Фамилия автора")
    date_of_birth: date = Field(..., description="Дата рождения")


class BookCreate(BookBase):
    pass


class AuthorCreate(AuthorBase):
    pass


class BookResponse(BookBase):
    id: int


class AuthorResponse(AuthorBase):
    id: int
