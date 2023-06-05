from typing import List

from func_call_patcher import validators

from .register import __func_call_patcher_register__
from .utils import FuncAsObjectFromStringGetter, FuncInvalidArgs


class FuncPathIsDuplicatedException(validators.BaseValidatationException):
    pass


class DecoratorInnerFuncIsIncorrect(validators.BaseValidatationException):
    pass


class FuncPathIsDuplicatedValidator(validators.IValidator):

    obj: str

    def validate(self) -> None:
        for func_patch_data in __func_call_patcher_register__.data.values():
            if func_patch_data.path_to_func_in_executable_module == self.obj:
                raise FuncPathIsDuplicatedException(
                    f"Патч на функцию по пути {self.obj} уже есть, мы не можем запатчить одну и ту же функцию дважды",
                )


class DecoratorInnerFuncIncorrectValidator(validators.IValidator):

    obj: str

    def validate(self) -> None:
        try:
            FuncAsObjectFromStringGetter.exec(func_as_str=self.obj)
        except FuncInvalidArgs as e:
            raise e
        except Exception:
            raise DecoratorInnerFuncIsIncorrect("decorator_inner_func не является валидной")


def validate(
    decorator_inner_func_as_str: str,
    is_method: bool,
    path_to_func_in_executable_module: str,
    line_number_where_func_executed: int,
) -> None:
    validators.validate(
        line_number_where_func_executed=line_number_where_func_executed,
        path_to_func_in_executable_module=path_to_func_in_executable_module,
        is_method=is_method,
    )
    validators_ext: List[validators.IValidator] = [
        FuncPathIsDuplicatedValidator(obj=path_to_func_in_executable_module),
        DecoratorInnerFuncIncorrectValidator(obj=decorator_inner_func_as_str),
    ]
    for validator in validators_ext:
        validator.validate()
