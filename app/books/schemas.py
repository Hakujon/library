from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    id: int
    name: str = Field(..., description="Название книги")
    description: Optional[str] = Field(
        None, max_length=500, description="Описание книги"
    )
    date_publication: date = Field(..., description="Дата публикации книги")
    author_id: int = Field(..., ge=1, description="ID автора книги")
