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

    def __str__(self):
        return (
            f"{self.__class__.__name__} (id={self.id})"
            f"{self.name}"
        )

    def __repr__(self):
        return str(self)


class Author(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]

    def __str__(self):
        return (
            f"{self.__class__.__name__} (id={self.id})"
            f"{self.first_name} {self.last_name}"
            f"{self.date_of_birth}"
        )