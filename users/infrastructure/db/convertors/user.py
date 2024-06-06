from users.infrastructure.db.models.users import User
from users.transfer.user import UserDTO, ToCreateUserDTO, UserFullDTO


def convert_user_dbmodel_to_dto(user: User) -> UserDTO | None:
    if not user:
        return

    return UserDTO(
        oid=user.id,
        email=user.email,
        username=user.username,
        about_me=user.about_me,
    )


def convert_user_dbmodel_to_full_dto(user: User) -> UserDTO | None:
    if not user:
        return

    return UserFullDTO(
        oid=user.id,
        email=user.email,
        username=user.username,
        about_me=user.about_me,
        hash_password=user.hash_password,
    )

def convert_created_user_to_dbmodel(user: ToCreateUserDTO, hash_password: str) -> User:

    return User(
        email=user.email,
        username=user.username,
        about_me=user.about_me,
        hash_password=hash_password,
    )
