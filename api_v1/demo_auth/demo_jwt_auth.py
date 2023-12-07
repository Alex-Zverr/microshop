from users.schemas import UserSchema

from auth import utils as auth_utils

john = UserSchema(
    usersname="John",
    password=auth_utils.hash_password("qwerty"),
    email="john@mail.ru"
)
sam = UserSchema(
    usersname="Sam",
    password=auth_utils.hash_password("secret")
)

users_db: dict[str, UserSchema] = {

}
