from typing import List

from func_call_patcher import validators

from .utils import FuncAsObjectFromStringGetter, FuncInvalidArgs


class DecoratorInnerFuncIsIncorrect(validators.BaseValidatationException):
    pass


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
    path_to_func: str,
    executable_module_name: str,
    line_number_where_func_executed: int,
) -> None:
    validators.validate(
        line_number_where_func_executed=line_number_where_func_executed,
        executable_module_name=executable_module_name,
        path_to_func=path_to_func,
        is_method=is_method,
    )
    validators_ext: List[validators.IValidator] = [
        DecoratorInnerFuncIncorrectValidator(obj=decorator_inner_func_as_str),
    ]
    for validator in validators_ext:
        validator.validate()
