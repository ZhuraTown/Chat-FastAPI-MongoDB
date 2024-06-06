import pytest
from pymongo.errors import DuplicateKeyError

from users.infrastructure.db.models.users import User


class TestUserModel:

    async def test_create_user(
            self,
            get_user_data: dict,

    ):
        user = User(**get_user_data)

        await user.insert()

        assert user
        assert user.id
        assert user.email == get_user_data["email"]
        assert user.username == get_user_data["username"]
        assert user.about_me == get_user_data["about_me"]
        assert user.hash_password == get_user_data["hash_password"]
        assert user.created_at

    async def test_create_user_without_about_me(
            self,
            get_user_data: dict,

    ):
        get_user_data["about_me"] = None
        user = User(**get_user_data)

        await user.insert()

        assert user
        assert user.id
        assert user.email == get_user_data["email"]
        assert user.username == get_user_data["username"]
        assert user.about_me == get_user_data["about_me"]
        assert user.hash_password == get_user_data["hash_password"]
        assert user.created_at

    async def test_cant_create_not_unique_username(
            self,
            get_user: User,
            get_user_data: dict,
    ):
        get_user_data["username"] = get_user.username
        user = User(**get_user_data)

        with pytest.raises(DuplicateKeyError):
            await user.insert()

    async def test_cant_create_not_unique_email(
            self,
            get_user: User,
            get_user_data: dict,
    ):
        get_user_data["email"] = get_user.email
        user = User(**get_user_data)

        with pytest.raises(DuplicateKeyError):
            await user.insert()

    async def test_get_user(
            self,
            get_user: User,
    ):
        founded_user = await User.get(get_user.id)

        assert founded_user
        assert founded_user.id == get_user.id
        assert founded_user.email == get_user.email
        assert founded_user.username == get_user.username
        assert founded_user.about_me == get_user.about_me
        assert founded_user.hash_password == get_user.hash_password

