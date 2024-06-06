from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from application.services.interfaces.user import UserServiceI
from presentation.api.controllers import PaginatedResponse, lo_paginator, LimitOffsetPaginator
from users.presentation.api.controllers.requests.user import (
    CreateUserRequest,
    get_user_filters,
    GetUserFilterRequest,
    UpdateUserRequest,
)
from users.presentation.api.controllers.responses.user import UserResponse
from users.presentation.api.deps.auth import get_current_user
from users.presentation.api.deps.services import get_user_service
from transfer.user import UserDTO


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    description="Регистрация",
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
)
async def register_user(
    new_user: CreateUserRequest,
    service: Annotated[UserServiceI, Depends(get_user_service)],
):
    user = await service.create(new_user.convert_to_dto())
    return user


@router.get(
    "/",
    description="Получить пользователей",
    response_model=PaginatedResponse,
    status_code=HTTPStatus.OK,
    dependencies=[Depends(get_current_user)],
)
async def get_users(
        filters: Annotated[GetUserFilterRequest, Depends(get_user_filters)],
        service: Annotated[UserServiceI, Depends(get_user_service)],
        paginator: Annotated[LimitOffsetPaginator[UserResponse], Depends(lo_paginator)],

):
    count = await service.count(filters=filters.convert_to_dto())
    users = await service.list(filters=filters.convert_to_dto(limit=paginator.limit, offset=paginator.offset))
    return paginator.paginate(users, count=count, model=UserResponse)


@router.get(
    "/me",
    description="Получить данные о себе",
    response_model=UserResponse,
    status_code=HTTPStatus.OK,
)
async def details_user(
        user: Annotated[UserDTO, Depends(get_current_user)],
):
    return user


@router.put(
    "/me",
    description="Обновить данные пользователя",
    response_model=UserResponse,
    status_code=HTTPStatus.OK,
)
async def update_user(
        update_data: UpdateUserRequest,
        service: Annotated[UserServiceI, Depends(get_user_service)],
        user: Annotated[UserDTO, Depends(get_current_user)],
):
    return await service.update(user.oid, update_data.convert_to_dto())


@router.delete(
    "/me",
    description="Деактивировать пользователя",
    status_code=HTTPStatus.OK,
)
async def soft_delete_user(
        service: Annotated[UserServiceI, Depends(get_user_service)],
        user: Annotated[UserDTO, Depends(get_current_user)],
):
    await service.soft_delete(user.oid)


@router.get(
    "/{user_id}",
    description="Получить пользователя",
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(get_current_user)],
)
async def get_user(
        user_id: UUID,
        service: Annotated[UserServiceI, Depends(get_user_service)],
):
    user = await service.get(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return user
