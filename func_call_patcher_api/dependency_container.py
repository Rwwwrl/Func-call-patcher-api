from dependency_injector import containers, providers

from func_call_patcher_api.logic.register import InMemoryFuncCallPatcherDataRegister


class DependencyContainer(containers.DeclarativeContainer):
    func_call_patcher_data_register = providers.Singleton(InMemoryFuncCallPatcherDataRegister)


__dependency_container__ = DependencyContainer()
