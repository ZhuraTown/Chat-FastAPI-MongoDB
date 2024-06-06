from typing import Protocol, List
from uuid import UUID


class CreateServiceInterfaceMixin[E, V](Protocol):

    async def create(self, entity: E, **kwargs) -> V: raise NotImplementedError


class UpdateServiceInterfaceMixin[U, V](Protocol):

    async def update(self, oid: UUID, update_data: U, **kwargs) -> V: raise NotImplementedError


class GetServiceInterfaceMixin[V](Protocol):

    async def get(self, oid: UUID, **kwargs) -> V | None: raise NotImplementedError


class ListServiceInterfaceMixin[F, V](Protocol):

    async def list(self, filters: F, **kwargs) -> List[V]: raise NotImplementedError


class SoftDeleteServiceInterfaceMixin(Protocol):

    async def soft_delete(self, oid: UUID, **kwargs) -> None: raise NotImplementedError


class CountServiceInterfaceMixin[F](Protocol):

    async def count(self, filters: F, **kwargs) -> int: raise NotImplementedError
