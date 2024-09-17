import uuid
from datetime import datetime

from sqlmodel import Field, func

from template_project.models.validation import UserBase


class User(UserBase, table=True):
    __tablename__ = "users"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
