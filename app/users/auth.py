from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.users.models import User
from app.config import settings
from app.users.dao import UsersDAO


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
        plain_password: str, hashed_password: str
        ) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = settings.get_auth_data()
    encode_jwt = jwt.encode(
        to_encode,
        auth_data["secret_key"],
        algorithm=auth_data["algorithm"]
        )
    return encode_jwt


async def authenticate_user(
        email_user: EmailStr, password: str, db_session: AsyncSession
        ) -> User | None:

    user: User | None = await UsersDAO.find_one_or_none(
        session=db_session,
        email=email_user
        )
    if not user or verify_password(
        plain_password=password, hashed_password=user.password
    ) is False:
        return None
    return user
