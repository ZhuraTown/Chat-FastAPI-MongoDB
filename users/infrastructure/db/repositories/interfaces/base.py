from typing import Protocol, List
from uuid import UUID


class CreateRepositoryInterfaceMixin[E, V](Protocol):

    async def create(self, entity: E, **kwargs) -> V: raise NotImplementedError


class UpdateRepositoryInterfaceMixin[U, V](Protocol):

    async def update(self, oid: UUID, update_data: U, **kwargs) -> V: raise NotImplementedError


class GetRepositoryInterfaceMixin[V](Protocol):

    async def get(self, oid: UUID, **kwargs) -> V | None: raise NotImplementedError


class ListRepositoryInterfaceMixin[F, V](Protocol):

    async def list(self, filters: F, **kwargs) -> List[V]: raise NotImplementedError


class DeleteRepositoryInterfaceMixin(Protocol):

    async def delete(self, oid: UUID, **kwargs) -> None: raise NotImplementedError


class CountRepositoryInterfaceMixin[F](Protocol):

    async def count(self, filters: F, **kwargs) -> int: raise NotImplementedError
