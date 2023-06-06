from attrs import define

from func_call_patcher_api import hints


@define
class FuncCallPatcherData:

    is_active: bool
    path_to_func_in_executable_module: str
    line_number_where_func_executed: int
    is_method: bool
    decorator_inner_func_as_str: hints.DecoratorInnerFuncAsStr
