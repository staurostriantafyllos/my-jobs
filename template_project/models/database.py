import uuid
from datetime import datetime

from sqlmodel import Field, ForeignKeyConstraint, func

from template_project.models.validation import JobBase, UserBase


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


class Job(JobBase, table=True):
    __tablename__ = "jobs"  # type: ignore
    __table_args__ = (
        ForeignKeyConstraint(
            columns=["user_id"],
            refcolumns=["users.id"],
            name="jobs_user_id_fkey",
            ondelete="CASCADE",
        ),
    )
    id: int = Field(default=None, primary_key=True, index=True)
    user_id: uuid.UUID
    created_at: datetime = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default=None,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
