import abc
from typing import Dict, NewType

from attrs import define

FuncCallPatherId = NewType('FuncCallPatherId', int)


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


@define
class FuncCallPatcherData:

    is_active: bool
    path_to_func_in_executable_module: str
    line_number_where_func_executed: int
    is_method: bool
    decorator_inner_func_as_str: str


class IFuncCallPatcherRegister(abc.ABC):
    def __init__(self):
        self._data: Dict[FuncCallPatherId, FuncCallPatcherData] = {}

    @abc.abstractmethod
    def add(self, func_call_patcher_data: FuncCallPatcherData) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, pk: FuncCallPatherId) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def change_is_active_state(self, pk: FuncCallPatherId) -> None:
        raise NotImplementedError

    @abc.abstractproperty
    def data(self) -> Dict[FuncCallPatherId, FuncCallPatcherData]:
        raise NotImplementedError

    @abc.abstractproperty
    def active_data(self) -> Dict[FuncCallPatherId, FuncCallPatcherData]:
        raise NotImplementedError


class FuncCallPatcherRegister(IFuncCallPatcherRegister):
    """реализация, которая хранит все в питоновской памяти"""
    def add(self, func_call_patcher_data: FuncCallPatcherData) -> FuncCallPatherId:
        pk = PkGenerator.get_and_increase_pk()
        self.data[pk] = func_call_patcher_data
        return pk

    def remove(self, pk: FuncCallPatherId) -> None:
        try:
            del self.data[pk]
        except KeyError:
            raise NotFound(f'по ключу {pk} нет записи')

    def change_is_active_state(self, pk: FuncCallPatherId) -> None:
        try:
            func_call_patcher_data = self.data[pk]
        except KeyError:
            raise NotFound(f'по ключу {pk} нет записи')
        else:
            func_call_patcher_data.is_active = not func_call_patcher_data.is_active

    @property
    def data(self) -> Dict[FuncCallPatherId, FuncCallPatcherData]:
        return self._data

    @property
    def active_data(self) -> Dict[FuncCallPatherId, FuncCallPatcherData]:
        return {
            pk: func_call_patcher_data
            for (pk, func_call_patcher_data) in self.data.items() if func_call_patcher_data.is_active
        }


__func_call_patcher_register__ = FuncCallPatcherRegister()