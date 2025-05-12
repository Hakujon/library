from app.dao.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.users.models import User, Role


class UsersDAO(BaseDAO):
    model = User

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        new_user = cls.model(**values)
        default_role = await RolesDAO.find_one_or_none(
            session, name="user")
        new_user.roles.append(default_role)
        session.add(new_user)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        await session.refresh(new_user)
        return new_user


class RolesDAO(BaseDAO):
    model = Role
