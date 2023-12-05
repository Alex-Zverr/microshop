import secrets
import uuid
from typing import Annotated, Any
from time import time
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth", tags=['Demo Auth'])

username_to_password = {
    "admin": "admin",
    "john": "password"
}

security = HTTPBasic()


@router.get('/basic-auth')
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password
    }


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> str:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Base"}
    )
    correct_password = username_to_password.get(credentials.username)
    if not correct_password:
        raise unauthed_exc

    # secrets
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8")
    ):
        raise unauthed_exc

    return credentials.username


@router.get('/basic-auth-username')
def demo_basic_auth_credentials(
    auth_username: str = Depends(get_auth_user_username)
):
    return {
        "message": f"Hi, {auth_username}",
        "username": auth_username,
    }


static_auth_to_username = {
    "b615d6fa5195d21dcb198fe14db8e47a": "admin",
    "5f47246483c6f6da4a86538c8df7abcf": "password"
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="static-auth-token")
) -> str:
    if token := static_auth_to_username.get(static_token):
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid"
    )


@router.get('/some-http-header-auth-username')
def demo_some_http_header_auth(
    auth_username: str = Depends(get_username_by_static_auth_token)
):
    return {
        "message": f"Hi, {auth_username}",
        "username": auth_username,
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIES_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(

):


@router.post('/login_cookie')
def login_set_cookie(
    response: Response,
    auth_username: str = Depends(get_auth_user_username)
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIES_SESSION_ID_KEY, session_id)
    return {"result": "ok"}

@router.get("/check-cookie")
def demo_auth_check_cookie():
    pass
