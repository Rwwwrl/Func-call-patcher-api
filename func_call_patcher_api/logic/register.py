import abc
from typing import Dict

from . import hints
from .value_objects import FuncCallPatcherData


class NotFound(BaseException):
    pass


class PkGenerator:

    _current_seq_value: int = 1

    @classmethod
    def get_and_increase_pk(cls) -> int:
        current_value = cls._current_seq_value
        current_value
        cls._current_seq_value += 1
        return current_value


class IFuncCallPatcherRegister(abc.ABC):
    def __init__(self):
        self._data: Dict[hints.FuncCallPatcherId, FuncCallPatcherData] = {}

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
    def add(self, func_call_patcher_data: FuncCallPatcherData) -> hints.FuncCallPatcherId:
        pk = PkGenerator.get_and_increase_pk()
        self.data[pk] = func_call_patcher_data
        return pk

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


__func_call_patcher_register__ = InMemoryFuncCallPatcherDataRegister()
