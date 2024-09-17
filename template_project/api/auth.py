from fastapi import HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import DecodeError, ExpiredSignatureError

from template_project.config import SecretAPISettings
from template_project.security import decode_jwt_token

secret_api_settings = SecretAPISettings()  # type: ignore


def verify_jwt_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing 'Bearer' prefix",
        )

    try:
        payload = decode_jwt_token(credentials.credentials)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )

    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    request.state.payload = payload
    return payload


def verify_api_token(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing 'Bearer' prefix",
        )

    if credentials.credentials != secret_api_settings.TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token"
        )

    return True
