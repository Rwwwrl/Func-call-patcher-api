import abc
from typing import Dict

from . import hints
from .value_objects import FuncCallPatcherData


class NotFound(BaseException):
    pass


class IFuncCallPatcherRegister(abc.ABC):
    @abc.abstractmethod
    def add(self, func_call_patcher_data: FuncCallPatcherData) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, pk: hints.FuncCallPatcherId) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def change_is_active_state(self, pk: hints.FuncCallPatcherId) -> None:
        raise NotImplementedError

    @abc.abstractproperty
    def data(self) -> Dict[hints.FuncCallPatcherId, FuncCallPatcherData]:
        raise NotImplementedError

    @abc.abstractproperty
    def active_data(self) -> Dict[hints.FuncCallPatcherId, FuncCallPatcherData]:
        raise NotImplementedError


class InMemoryFuncCallPatcherDataRegister(IFuncCallPatcherRegister):
    """реализация, которая хранит все в питоновской памяти"""
    def __init__(self):
        self._data: Dict[hints.FuncCallPatcherId, FuncCallPatcherData] = {}

    def add(self, func_call_patcher_data: FuncCallPatcherData) -> None:
        self.data[func_call_patcher_data.pk] = func_call_patcher_data

    def remove(self, pk: hints.FuncCallPatcherId) -> None:
        try:
            del self.data[pk]
        except KeyError:
            raise NotFound(f'по ключу {pk} нет записи')

    def change_is_active_state(self, pk: hints.FuncCallPatcherId) -> None:
        try:
            func_call_patcher_data = self.data[pk]
        except KeyError:
            raise NotFound(f'по ключу {pk} нет записи')
        else:
            func_call_patcher_data.is_active = not func_call_patcher_data.is_active

    @property
    def data(self) -> Dict[hints.FuncCallPatcherId, FuncCallPatcherData]:
        return self._data

    @property
    def active_data(self) -> Dict[hints.FuncCallPatcherId, FuncCallPatcherData]:
        return {
            pk: func_call_patcher_data
            for (pk, func_call_patcher_data) in self.data.items() if func_call_patcher_data.is_active
        }
