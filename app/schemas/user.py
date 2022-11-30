import re

from pydantic import BaseModel, EmailStr, Field, SecretStr, validator


class UserBase(BaseModel):
    username: str

    @validator("username")
    def username_regexp(cls, v: str) -> str:
        v = v.strip()
        if re.match(r"^[a-zA-Z0-9]+_?[a-zA-Z0-9]+$", v) is None:
            raise ValueError(
                "может содержать латинские символы, цифры, "
                "или знак подчёркивания."
                " Начинаться и заканчиваться только латинским символом",
            )
        return v


class AdvancedUser(UserBase):
    email: EmailStr


class Admin(BaseModel):
    is_admin: bool


class MyUser(AdvancedUser, Admin):
    id: int


class User(UserBase, Admin):
    id: int


class UserPassword(BaseModel):
    password: str

    @validator("password")
    def password_complexity(cls, v: str) -> str:
        min_length = 6
        if len(v) < 6:
            raise ValueError(f"минимальная длина пароля {min_length} символов")
        return v


class NewUserDto(AdvancedUser):
    hashed_password: str = Field(..., alias="password")


class CreateUser(AdvancedUser, UserPassword):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
