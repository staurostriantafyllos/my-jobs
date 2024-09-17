import uuid

from sqlmodel import Session, select

from template_project.models.database import User
from template_project.models.validation import UserCreate, UserUpdate
from template_project.security import get_password_hash, verify_password


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def get_user_by_id(session: Session, user_id: uuid.UUID) -> User | None:
    return session.get(User, user_id)


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_user(session: Session, user_in: UserCreate) -> User:
    user = User.model_validate(
        user_in, update={"hashed_password": get_password_hash(user_in.password)}
    )

    session.add(user)
    session.flush()
    session.refresh(user)

    return user


def update_user(
    session: Session, user_in: UserUpdate, user_id: uuid.UUID
) -> User | None:
    db_user = session.get(User, user_id)

    if not db_user:
        return None

    user_data = user_in.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)

    session.add(db_user)
    session.flush()
    session.refresh(db_user)

    return db_user
