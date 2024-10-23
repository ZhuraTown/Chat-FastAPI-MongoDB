from uuid import UUID

from users.application.services.interfaces.base import (
    CreateServiceInterfaceMixin,
    UpdateServiceInterfaceMixin,
    GetServiceInterfaceMixin,
    ListServiceInterfaceMixin,
    SoftDeleteServiceInterfaceMixin,
    CountServiceInterfaceMixin,
)
from users.transfer.user import (
    ToCreateUserDTO,
    UserDTO,
    UpdateUserDTO,
    FilterUserDTO, UpdateUserPasswordDTO,
)


class UserServiceI(
    CreateServiceInterfaceMixin[ToCreateUserDTO, UserDTO],
    UpdateServiceInterfaceMixin[UpdateUserDTO, UserDTO],
    GetServiceInterfaceMixin[UserDTO],
    ListServiceInterfaceMixin[FilterUserDTO, UserDTO],
    SoftDeleteServiceInterfaceMixin,
    CountServiceInterfaceMixin[FilterUserDTO],
):
    async def change_password(
            self,
            user_id: UUID,
            update_data: UpdateUserPasswordDTO,
    ) -> UserDTO:
        raise NotImplementedError

    async def authenticate(
            self,
            username: str,
            password: str,
    ) -> UserDTO | None:
        raise NotImplementedError
