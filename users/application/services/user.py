from uuid import UUID

from application.auth.hashing import get_password_hash, verify_password_and_update
from users.infrastructure.db.convertors.user import convert_created_user_to_dbmodel
from users.infrastructure.db.repositories.interfaces.user import UserRepositoryI

from users.application.services.exceptions.user import (
    EmailAlreadyExistError,
    UserNotExistError,
    UsernameAlreadyExistError,
)
from users.transfer.user import (
    UserDTO,
    ToCreateUserDTO,
    UpdateUserDataDTO,
    UpdateUserPasswordDTO,
    FilterUserDTO,
)


class ValidateUserDataMixin:
    _user_repository: UserRepositoryI

    async def validate_user_data(self, user_data: ToCreateUserDTO):

        if await self._user_repository.get_user_by_email(user_data.email):
            raise EmailAlreadyExistError(user_data.email)

        if await self._user_repository.get_user_by_username(user_data.username):
            raise UsernameAlreadyExistError(user_data.username)


class UserService(
    ValidateUserDataMixin,
):

    def __init__(self, user_repository):
        self._user_repository: UserRepositoryI = user_repository

    async def count(
            self,
            filters: FilterUserDTO,
    ) -> int:
        count = await self._user_repository.count(filters)
        return count

    async def create(
            self,
            user_data: ToCreateUserDTO,
    ) -> UserDTO:

        await self.validate_user_data(user_data)
        user = await self._user_repository.create(
            convert_created_user_to_dbmodel(user_data, get_password_hash(user_data.password)),
        )
        return user

    async def get(
            self,
            oid: UUID,
    ) -> UserDTO | None:
        user = await self._user_repository.get(oid)
        if not user:
            raise UserNotExistError(oid)
        return user

    async def update(
            self,
            oid: UUID,
            update_data: UpdateUserDataDTO,
    ) -> UserDTO:
        user = await self._user_repository.get(id)
        if not user:
            raise UserNotExistError(id)
        await self._user_repository.update(id, update_data)
        return await self.get(id)

    async def list(
            self,
            filters: FilterUserDTO,
    ) -> list[UserDTO]:
        users = await self._user_repository.list(filters)
        return users

    async def soft_delete(
            self,
            oid: UUID,
    ):
        user = await self._user_repository.get(id)
        if not user:
            raise UserNotExistError(id)
        await self._user_repository.delete(id)

    async def change_password(
            self,
            user_id: UUID,
            update_data: UpdateUserPasswordDTO,
    ) -> UserDTO:
        user = await self._user_repository.get(user_id)
        if not user:
            raise UserNotExistError(user_id)
        await self._user_repository.update(user_id, update_data)
        return await self.get(user_id)

    async def authenticate(
            self,
            username: str,
            password: str,
    ) -> UserDTO | None:

        user = await self._user_repository.get_user_by_username(username)
        if not user:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            get_password_hash(password)
            return None

        verified, updated_password_hash = verify_password_and_update(password, user.hash_password)
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self._user_repository.update(
                user.id, UpdateUserPasswordDTO(hash_password=updated_password_hash),
            )
        return user



