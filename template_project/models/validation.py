import uuid

from pydantic import EmailStr
from sqlmodel import AutoString, Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255, sa_type=AutoString)
    first_name: str
    last_name: str


class UserUpdate(SQLModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserLogin(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)


class UserPublic(UserBase):
    id: uuid.UUID


class TokenResponse(SQLModel):
    access_token: str
