from contextlib import contextmanager

from sqlalchemy.engine import URL, Engine
from sqlmodel import Session, create_engine

from template_project.config import DatabaseSettings, SecretDatabaseSettings

config = DatabaseSettings()  # type: ignore
secret = SecretDatabaseSettings()  # type: ignore

engine = None


def create_database_engine() -> Engine:
    connection_string = URL.create(
        "postgresql",
        username=secret.USER,
        password=secret.PASSWORD,
        host=config.HOSTNAME,
        database=config.DATABASE,
        port=config.PORT,
    )

    connect_args = {}

    engine = create_engine(
        connection_string,
        connect_args=connect_args,
        pool_size=config.POOL_SIZE,
        max_overflow=config.MAX_OVERFLOW,
        pool_recycle=config.POOL_RECYCLE,
        pool_pre_ping=config.POOL_PRE_PING,
        pool_use_lifo=config.POOL_USE_LIFO,
        echo=config.ECHO,
    )
    return engine


def get_db_session():
    global engine
    if not engine:
        engine = create_database_engine()

    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()  # Rollback in case of an error
        raise
    finally:
        session.close()


@contextmanager
def get_session_ctx():
    yield from get_db_session()
