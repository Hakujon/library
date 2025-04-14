from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date

from app.database import Base, int_pk, str_uniq, str_null


class Book(Base):
    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    description: Mapped[str_null]
    date_publication: Mapped[date]
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id"), nullable=False
    )
    author: Mapped["Author"] = relationship(
        "Author", back_populates="students"
    )


class Author(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
