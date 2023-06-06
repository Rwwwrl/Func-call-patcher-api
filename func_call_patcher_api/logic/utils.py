import re
from typing import Callable

from func_call_patcher.validators import BaseValidatationException


class FuncInvalidArgs(BaseValidatationException):
    pass


class FuncAsObjectFromStringGetter:
    @staticmethod
    def _get_name_of_func_from_str(func_as_str: str) -> str:
        first_line = func_as_str.split("\n")[0]
        pattern = re.compile("(?<=def )(.*?)(?=\()")    # noqa
        name_of_func = re.findall(pattern, first_line)[0]
        return name_of_func

    @staticmethod
    def _validate_args(func: Callable):
        valid_args = ('func', 'func_args', 'func_kwargs', 'frame', 'relationship_identifier')
        func_args = func.__code__.co_varnames
        if func_args != valid_args:
            raise FuncInvalidArgs(f"Аргументы у переданной функции должны быть {valid_args}, сейчас {func_args}")

    @classmethod
    def exec(cls, func_as_str: str) -> Callable:
        func_name = cls._get_name_of_func_from_str(func_as_str)
        exec(func_as_str)
        func = locals()[func_name]
        cls._validate_args(func)
        return func
