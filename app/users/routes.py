from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Response
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.users.auth import get_password_hash, authenticate_user
from app.users.auth import create_access_token
from app.users.models import User
from app.users.dao import UsersDAO, RolesDAO
from app.users.schemas import UserRegistry, UserResponse, UserAuth
from app.users.schemas import RoleCreate, RoleResponse
from app.database import DB_SESSION
from app.users.dependencies import get_current_user, check_admin_role, check_role_sportsman

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def create_user(user_data: UserRegistry, db_session: DB_SESSION) -> dict:
    user = await UsersDAO.find_one_or_none(db_session, email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already created"
        )
    user_data.password = get_password_hash(user_data.password)
    user_db = await UsersDAO.add(db_session, **user_data.model_dump())
    return {
        "message": "User was created",
        "user": UserResponse.model_validate(user_db)
    }


# @router.post("/login")
# async def auth_user(
#         response: Response, user_data: UserAuth, db_session: DB_SESSION):
#     user = await authenticate_user(
#         email_user=user_data.email,
#         password=user_data.password,
#         db_session=db_session)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Неверная почта или пароль")
#     access_token = create_access_token({"sub": str(user.id)})
#     response.set_cookie(
#         key="users_access_token", value=access_token, httponly=True
#         )
#     return {"access_token": access_token, "refresh_token": None}


@router.post("/login")
async def auth_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                    db_session: DB_SESSION):
    user = await authenticate_user(
        email_user=form_data.username,
        password = form_data.password,
        db_session=db_session
    )
    if user is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Неверная почта или пароль")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token,
            "token_type": "bearer"}


@router.get("/me")
async def get_me(user_data: Annotated[User, Depends(get_current_user)]):
    return UserResponse.model_validate(user_data)


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Logout successfull"}


@router.post("/role")
async def create_role(role_data: RoleCreate,
                      db_session: DB_SESSION):
    role = await RolesDAO.find_one_or_none(db_session, name=role_data.name)
    if role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role is already created"
        )
    role_db = await RolesDAO.add(db_session, **role_data.model_dump())
    return {"message": "Role was created",
            "role": RoleResponse.model_validate(role_db)
            }


@router.get("/role")
async def get_all_roles(user: Annotated[User, Depends(check_admin_role)],
                        db_session: DB_SESSION):
    roles = await RolesDAO.find_all(db_session)
    return [RoleResponse.model_validate(role) for role in roles]


@router.get("/role/shtanga")
async def get_shtanga(user: Annotated[User, Depends(check_role_sportsman)],
                      db_session: DB_SESSION):
    return {"message":
            "ШТАНГА ПОДНЯТА, УРА, УРА!"}


@router.post("/assign_role/{user_id}")
async def give_role(user_id: int, role_name: str, db_session: DB_SESSION):
    user: User | None = await UsersDAO.find_one_by_id(db_session, user_id)
    role = await RolesDAO.find_one_or_none(db_session, name=role_name)
    if role in user.roles:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has role"
        )
    user.roles.append(role)
    await db_session.commit()
    return {
        "message": "Role was assigned"
    }
