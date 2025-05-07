from fastapi import APIRouter, HTTPException, status, Response
from app.users.auth import get_password_hash, authenticate_user
from app.users.auth import create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import UserRegistry, UserResponse, UserAuth
from app.database import DB_SESSION


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def create_user(user_data: UserRegistry, db_session: DB_SESSION) -> dict:
    user = await UsersDAO.find_one_or_none(db_session, email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already created"
        )
    user_dict = user_data.model_dump()
    print(user_dict)
    user_dict["password"] = get_password_hash(user_data.password)
    user_db = await UsersDAO.add(db_session, **user_dict)
    return {
        "message": "User was created",
        "user": UserResponse.model_validate(user_db)
    }


@router.post("/login")
async def auth_user(
        response: Response, user_data: UserAuth, db_session: DB_SESSION):
    user = await authenticate_user(
        email_user=user_data.email,
        password=user_data.password,
        db_session=db_session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверная почта или пароль")
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="users_access_token", value=access_token, httponly=True
        )
    return {"access_token": access_token, "refresh_token": None}
