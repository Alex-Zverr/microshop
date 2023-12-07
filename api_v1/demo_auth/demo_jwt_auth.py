from fastapi import APIRouter, Depends

from pydantic import BaseModel

from auth import utils as auth_utils
from users.schemas import UserSchema


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT"])

john = UserSchema(
    username="John",
    password=auth_utils.hash_password("qwerty"),
    email="john@mail.ru"
)
sam = UserSchema(
    username="Sam",
    password=auth_utils.hash_password("secret")
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user():
    pass


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )
