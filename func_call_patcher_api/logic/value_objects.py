from attrs import define, field

from func_call_patcher_api import hints

from .utils import PkGenerator


@define
class FuncCallPatcherData:

    pk: hints.FuncToPatchKwargs = field(factory=PkGenerator.get_and_increase_pk, init=False)
    is_active: bool
    path_to_func_in_executable_module: str
    line_number_where_func_executed: int
    is_method: bool
    decorator_inner_func_as_str: hints.DecoratorInnerFuncAsStr
