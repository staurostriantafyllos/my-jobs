from fastapi import Depends

from template_project.api.auth import verify_jwt_token
from template_project.db.factories import get_db_session


def get_session():
    yield from get_db_session()


def get_session_by_user(payload: dict = Depends(verify_jwt_token)):
    yield from get_db_session()
