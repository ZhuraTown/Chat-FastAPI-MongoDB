import pytest
from faker import Faker

from users.infrastructure.db.models.users import User
from users.infrastructure.db.repositories.interfaces.user import UserRepositoryI
from users.transfer.user import UserDTO, UpdateUserDataDTO, UpdateUserPasswordDTO, FilterUserDTO


class TestUserRepository:

    async def test_create_user(
            self,
            get_user_data: dict,
            get_repository_user: UserRepositoryI,

    ):
        user = User(**get_user_data)
        created_user = await get_repository_user.create(user)

        assert created_user
        assert created_user.oid
        assert created_user.email == user.email
        assert created_user.username == user.username
        assert created_user.about_me == user.about_me
        assert isinstance(created_user, UserDTO)

    async def test_get_user(
            self,
            get_user: User,
            get_repository_user: UserRepositoryI,
    ):
        founded_user = await get_repository_user.get(get_user.id)

        assert founded_user
        assert founded_user.oid
        assert founded_user.email == get_user.email
        assert founded_user.username == get_user.username
        assert founded_user.about_me == get_user.about_me
        assert isinstance(founded_user, UserDTO)

    @pytest.mark.parametrize("about_me", [None, "about_me info"])
    async def test_update_user_data(
            self,
            get_user: User,
            get_repository_user: UserRepositoryI,
            about_me,
    ):
        data = UpdateUserDataDTO(about_me=about_me)

        updated_user = await get_repository_user.update(get_user.id, data)

        assert updated_user
        assert updated_user.about_me == about_me
        assert isinstance(updated_user, UserDTO)
    
    async def test_update_user_password(
            self,
            get_user: User,
            get_repository_user: UserRepositoryI,
            faker: Faker,
    ):
        data = UpdateUserPasswordDTO(hash_password=faker.password())

        await get_repository_user.update(get_user.id, data)
        updated_user = await User.get(get_user.id)

        assert updated_user.hash_password == data.hash_password

    async def test_list_users(
            self,
            get_user: User,
            get_repository_user: UserRepositoryI,
    ):
        filters = FilterUserDTO(limit=5, offset=0)

        users = await get_repository_user.list(filters)

        assert users
        assert isinstance(users[0], UserDTO)

    async def test_delete_user(
            self,
            get_user: User,
            get_repository_user: UserRepositoryI,
    ):
        deleted_user = await get_repository_user.delete(get_user.id)

        assert not deleted_user

    async def test_soft_delete_user(
            self,
            get_user: User,
            get_repository_user: UserRepositoryI,
    ):
        deleted_user = await get_repository_user.delete(get_user.id)
        user_from_db = await User.get(get_user.id)

        assert not deleted_user
        assert user_from_db.deleted_at

    async def test_get_user_by_email(
            self,
            get_user: User,
            get_repository_user: UserRepositoryI,
    ):
        founded_user = await get_repository_user.get_user_by_email(get_user.email)

        assert founded_user
        assert founded_user.email == get_user.email
        assert isinstance(founded_user, UserDTO)

    async def test_get_user_by_username(
            self,
            get_user: User,
            get_repository_user: UserRepositoryI,
    ):
        founded_user = await get_repository_user.get_user_by_username(get_user.username)

        assert founded_user
        assert founded_user.username == get_user.username
        assert isinstance(founded_user, UserDTO)


