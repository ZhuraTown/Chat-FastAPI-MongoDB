from users.infrastructure.db.models.users import User
from users.infrastructure.db.repositories.interfaces.base import (
    CreateRepositoryInterfaceMixin,
    UpdateRepositoryInterfaceMixin,
    GetRepositoryInterfaceMixin,
    ListRepositoryInterfaceMixin,
    DeleteRepositoryInterfaceMixin, CountRepositoryInterfaceMixin,
)
from users.transfer.user import (UserDTO, UpdateUserDTO, FilterUserDTO, UserFullDTO)


class UserRepositoryI(
    CreateRepositoryInterfaceMixin[User, UserDTO],
    UpdateRepositoryInterfaceMixin[UpdateUserDTO, UserDTO],
    GetRepositoryInterfaceMixin[UserDTO],
    ListRepositoryInterfaceMixin[FilterUserDTO, UserDTO],
    DeleteRepositoryInterfaceMixin,
    CountRepositoryInterfaceMixin,
):
    async def get_user_by_email(
            self,
            email: str,
    ) -> UserFullDTO | None:
        raise NotImplementedError

    async def get_user_by_username(
            self,
            username: str,
    ) -> UserFullDTO | None:
        raise NotImplementedError
