from dependency_injector import containers, providers

from func_call_patcher_api.logic.repository import InMemoryRepository


class DependencyContainer(containers.DeclarativeContainer):
    repository_factory = providers.Singleton(InMemoryRepository)


__dependency_container__ = DependencyContainer()
