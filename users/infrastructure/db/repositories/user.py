from uuid import UUID
from datetime import datetime, UTC

from beanie.odm.operators.update.general import Set

from users.infrastructure.db.convertors.user import (
    convert_user_dbmodel_to_dto,
    convert_user_dbmodel_to_full_dto,
)
from users.infrastructure.db.models.users import User
from users.transfer.user import UserDTO, UpdateUserDTO, FilterUserDTO


class UserRepository:
    async def create(
            self,
            user: User,
    ) -> UserDTO:
        await user.insert()
        return await self.get(user.id)

    async def get(
            self,
            oid,
    ) -> UserDTO | None:
        search_criteria = {User.id: oid, User.deleted_at: None}
        user = await User.find(search_criteria).first_or_none()
        return convert_user_dbmodel_to_dto(user)

    async def update(
            self,
            oid: UUID,
            update_data: UpdateUserDTO,
    ) -> UserDTO:
        search_criteria = {User.id: oid, User.deleted_at: None}
        user = await User.find(search_criteria).first_or_none()
        await user.set(update_data.get_data())
        return await self.get(oid)

    async def list(
            self,
            filters: FilterUserDTO,
    ) -> list[UserDTO]:
        search_criteria = {User.deleted_at: None}
        users = await User.find(search_criteria, limit=filters.limit, skip=filters.offset).to_list()
        return [convert_user_dbmodel_to_dto(user) for user in users]

    async def delete(
            self,
            oid: UUID,
    ):
        user = await User.find(User.id == oid).first_or_none()
        await user.update(Set({User.deleted_at: datetime.now(tz=UTC)}))

    async def get_user_by_email(
            self,
            email: str,
    ) -> UserDTO | None:
        user = await User.find(User.email == email).first_or_none()
        return convert_user_dbmodel_to_full_dto(user)

    async def get_user_by_username(
            self,
            username: str,
    ) -> UserDTO | None:
        user = await User.find(User.username == username).first_or_none()
        return convert_user_dbmodel_to_full_dto(user)

    async def count(
            self,
            filters: FilterUserDTO,
    ) -> int:
        search_criteria = {User.deleted_at: None}
        count = await User.find(search_criteria).count()
        return count
