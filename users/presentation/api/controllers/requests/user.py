from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from transfer.user import ToCreateUserDTO, FilterUserDTO, UpdateUserDataDTO


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=64)
    about_me: Optional[str]
    password: str = Field(..., min_length=8, max_length=64)

    def convert_to_dto(self) -> ToCreateUserDTO:
        return ToCreateUserDTO(
            email=self.email,
            username=self.username,
            about_me=self.about_me,
            password=self.password,
        )


class UpdateUserRequest(BaseModel):
    about_me: Optional[str]

    def convert_to_dto(self) -> UpdateUserDataDTO:
        return UpdateUserDataDTO(about_me=self.about_me)


class GetUserFilterRequest(BaseModel):
    search: str | None = None

    def convert_to_dto(
            self,
            limit: int | None = None,
            offset: int | None = None,
    ) -> FilterUserDTO:
        return FilterUserDTO(limit=limit, offset=offset, search=self.search)


def get_user_filters(
        search: str | None = None,

) -> GetUserFilterRequest:
    return GetUserFilterRequest(search=search)
