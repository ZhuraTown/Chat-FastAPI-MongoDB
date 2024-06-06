from abc import ABC, abstractmethod
from typing import Sequence, Self

from fastapi import Request
from pydantic import BaseModel, HttpUrl
from starlette.datastructures import URL


class BaseResponse(ABC, BaseModel):

    @abstractmethod
    def convert_from_dto(self, dto) -> Self:
        ...


class PaginatedResponse[T: BaseResponse](
    BaseModel,
):
    results: Sequence[T]
    next: HttpUrl | None = None
    previous: HttpUrl | None = None
    count: int


class LimitOffsetPaginator[T]:
    def __init__(self):
        self._url: URL | None = None
        self.count: int | None = None
        self.limit = None
        self.offset = None

    def __call__(self, request: Request, limit: int | None = 20, offset: int | None = 0) -> Self:
        self.limit = limit
        self.offset = offset
        self._url = request.url
        return self

    def get_next_url(self, count: int) -> str | None:
        if self.offset + self.limit >= count:
            return None

        return str(
            self._url.include_query_params(offset=self.offset + self.limit, limit=self.limit),
        )

    def get_previous_url(self) -> str | None:
        if self.offset <= 0:
            return None

        return str(
            self._url.include_query_params(offset=max(0, self.offset - self.limit), limit=self.limit),
        )

    def paginate(self, data, count: int, model: T) -> PaginatedResponse:
        return PaginatedResponse(
            results=[model.convert_from_dto(instance) for instance in data],
            next=self.get_next_url(count),
            previous=self.get_previous_url(),
            count=count,
        )


lo_paginator = LimitOffsetPaginator()