from abc import abstractmethod, ABC
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from users.infrastructure.db.models.users import User


class UserDTO(BaseModel):
    oid: UUID
    email: str
    username: str
    about_me: Optional[str]


class UserFullDTO(UserDTO):
    hash_password: str


class ToCreateUserDTO(BaseModel):
    email: str
    username: str
    about_me: Optional[str]
    password: str


class UpdateUserDTO(BaseModel, ABC):

    @abstractmethod
    def get_data(self):
        raise NotImplementedError


class UpdateUserDataDTO(UpdateUserDTO):
    about_me: Optional[str]

    def get_data(self):
        return {User.about_me: self.about_me}


class UpdateUserPasswordDTO(UpdateUserDTO):
    hash_password: str

    def get_data(self):
        return {User.hash_password: self.hash_password}


class FilterUserDTO(BaseModel):
    search: Optional[str] = None
    limit: int | None = None
    offset: int | None = None

