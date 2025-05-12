from typing import Annotated
from datetime import datetime, timezone
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from app.users.auth import oauth2_scheme
from app.database import DB_SESSION
from app.users.dao import UsersDAO, RolesDAO
from app.users.models import User, Role
from app.config import settings


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
            )
    return token


# async def get_current_user(token: Annotated[str, Depends(get_token)],
#                            db_session: DB_SESSION):
#     try:
#         auth_data = settings.get_auth_data()
#         payload = jwt.decode(token=token,
#                              key=auth_data["secret_key"],
#                              algorithms=[auth_data["algorithm"]])
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Token is not valid")

#     expire = payload.get("exp")
#     expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
#     if (not expire) or (expire_time < datetime.now(timezone.utc)):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Token is not valid")

#     user_id = payload.get("sub")
#     if not user_id:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="User ID not found")
#     user = await UsersDAO.find_one_by_id(db_session, int(user_id))
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="User not found")

#     return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db_session: DB_SESSION):
    try:
        auth_data = settings.get_auth_data()
        payload = jwt.decode(token=token,
                             key=auth_data["secret_key"],
                             algorithms=[auth_data["algorithm"]])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token is not valid",
                            headers={"WWW-Athenticate": "Bearer"})
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User ID not found")
    user = await UsersDAO.find_one_by_id(db_session, int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")
    return user


async def check_admin_role(user: Annotated[User, Depends(get_current_user)],
                           db_session: DB_SESSION):
    admin_role = await RolesDAO.find_one_or_none(db_session, name="admin")
    if admin_role not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have no permission"
        )
    return user


async def check_role_sportsman(
        user: Annotated[User, Depends(get_current_user)],
        db_session: DB_SESSION):
    sportsman_role = await RolesDAO.find_one_or_none(
        db_session, name="sportsman"
        )
    if sportsman_role not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have no permission"
        )
    return user
