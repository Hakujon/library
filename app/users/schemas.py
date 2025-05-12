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


class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ..., min_length=3, description="Название роли"
    )


class UserRegistry(UserBase):
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль 5-50 знаков"
        )


class RoleCreate(RoleBase):
    pass


class UserResponse(UserBase):
    id: int
    roles: list[RoleBase]


class RoleResponse(RoleBase):
    id: int


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль"
        )
