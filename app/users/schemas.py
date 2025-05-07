from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(
        ..., min_length=3, max_length=30, description="Имя  пользователя"
        )
    last_name: str = Field(
        ..., min_length=3, max_length=30, description="Фамилия пользователя"
        )
    email: EmailStr = Field(
        ..., description="Эл.почта пользователя"
        )
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль 5-50 знаков"
        )


class UserRegistry(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    password: str = Field(..., description="Пароль")


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль"
        )
