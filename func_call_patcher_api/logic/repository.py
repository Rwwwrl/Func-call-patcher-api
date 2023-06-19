import abc
from typing import Dict

from func_call_patcher_api import hints

from .func_call_patcher_data import FuncCallPatcherData
from .utils import PkGenerator


class NotFound(BaseException):
    pass


class IFuncCallPatcherRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, func_call_patcher_data: FuncCallPatcherData) -> hints.FuncCallPatcherId:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, pk: hints.FuncCallPatcherId) -> FuncCallPatcherData:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, pk: hints.FuncCallPatcherId) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def change_active_state_to_opposite(self, pk: hints.FuncCallPatcherId) -> None:
        raise NotImplementedError

    @abc.abstractproperty
    def all(self) -> Dict[hints.FuncCallPatcherId, FuncCallPatcherData]:
        raise NotImplementedError

    @abc.abstractproperty
    def active(self) -> Dict[hints.FuncCallPatcherId, FuncCallPatcherData]:
        raise NotImplementedError


class InMemoryRepository(IFuncCallPatcherRepository):
    """реализация, которая хранит все в питоновской памяти"""
    def __init__(self):
        self._data: Dict[hints.FuncCallPatcherId, FuncCallPatcherData] = {}
        self.pk_generator = PkGenerator()

    def add(self, func_call_patcher_data: FuncCallPatcherData) -> hints.FuncCallPatcherId:
        pk = self.pk_generator.get_and_increase_pk()
        self._data[pk] = func_call_patcher_data
        return pk

    def get(self, pk: hints.FuncCallPatcherId) -> FuncCallPatcherData:
        try:
            return self._data[pk]
        except KeyError:
            raise NotFound(f'по ключу {pk} нет записи')

    def delete(self, pk: hints.FuncCallPatcherId) -> None:
        try:
            del self._data[pk]
        except KeyError:
            raise NotFound(f'по ключу {pk} нет записи')

    def change_active_state_to_opposite(self, pk: hints.FuncCallPatcherId) -> None:
        func_call_patcher_data = self.get(pk=pk)
        func_call_patcher_data.is_active = not func_call_patcher_data.is_active

    @property
    def all(self) -> Dict[hints.FuncCallPatcherId, FuncCallPatcherData]:
        return self._data

    @property
    def active(self) -> Dict[hints.FuncCallPatcherId, FuncCallPatcherData]:
        return {
            pk: func_call_patcher_data
            for (pk, func_call_patcher_data) in self.all.items() if func_call_patcher_data.is_active
        }
