from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from template_project.api.auth import verify_jwt_token
from template_project.api.dependencies import get_session, get_session_by_user
from template_project.db.controllers import accounts
from template_project.models.validation import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserPublic,
    UserUpdate,
)
from template_project.security import create_access_token

router = APIRouter(
    prefix="",
    tags=["accounts"],
)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def register_user(
    body: UserCreate, session: Session = Depends(get_session)
) -> Any:
    user = accounts.get_user_by_email(session=session, email=body.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system",
        )
    new_user = accounts.create_user(session=session, user_in=body)

    return new_user


@router.post("/login")
async def user_login(
    body: UserLogin,
    session: Session = Depends(get_session),
) -> TokenResponse:
    user = accounts.authenticate_user(
        session=session, email=body.email, password=body.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    token = create_access_token(subject=user.id)

    return TokenResponse(access_token=token)


@router.get("/accounts/me", response_model=UserPublic)
async def get_user_me(
    session: Session = Depends(get_session_by_user),
    payload: dict = Depends(verify_jwt_token),
) -> Any:
    user = accounts.get_user_by_id(session=session, user_id=payload['sub'])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.patch("/accounts/me", response_model=UserPublic)
async def update_user_me(
    body: UserUpdate,
    session: Session = Depends(get_session_by_user),
    payload: dict = Depends(verify_jwt_token),
) -> Any:
    user = accounts.update_user(session=session, user_in=body, user_id=payload['sub'])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
