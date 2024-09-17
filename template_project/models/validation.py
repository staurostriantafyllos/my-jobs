import uuid

from pydantic import EmailStr
from sqlmodel import AutoString, Field, SQLModel


class PaginationRequest(SQLModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1)


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


class JobBase(SQLModel):
    company_name: str
    job_title: str
    salary: float = Field(ge=0)


class JobResponse(JobBase):
    id: int


class JobsResponse(SQLModel):
    total: int
    data: list[JobResponse]


class JobsRequest(SQLModel):
    company_name: str | None = None
    salary: float | None = None
