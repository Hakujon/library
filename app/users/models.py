from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database import Base, str_uniq, int_pk


class User(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]
    roles: Mapped[list["Role"]] = relationship(
        secondary="userroles",
        back_populates="users",
        lazy="selectin"
    )

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__} (id={self.id})"


class Role(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    users: Mapped[list["User"]] = relationship(
        secondary="userroles",
        back_populates="roles"
    )


class UserRole(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True
        )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), primary_key=True
        )
