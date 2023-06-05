from typing import List

from func_call_patcher import FuncCallPatcher, MultiFuncCallPatcher

from func_call_patcher_api.logic.register import __func_call_patcher_register__
from func_call_patcher_api.logic.utils import FuncAsObjectFromStringGetter


class FuncCallPatcherMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        patchers: List[FuncCallPatcher] = []

        for func_call_patcher_data in __func_call_patcher_register__.active_data.values():
            decorator_inner_func = FuncAsObjectFromStringGetter.exec(
                func_as_str=func_call_patcher_data.decorator_inner_func_as_str,
            )
            patchers.append(
                FuncCallPatcher(
                    path_to_func_in_executable_module=func_call_patcher_data.path_to_func_in_executable_module,
                    line_number_where_func_executed=func_call_patcher_data.line_number_where_func_executed,
                    decorator_inner_func=decorator_inner_func,
                    is_method=func_call_patcher_data.is_method,
                ),
            )

        try:
            with MultiFuncCallPatcher(*patchers):
                return self.get_response(request)
        except Exception:
            # мы при любой ошибке должны обработать реквест должным образом
            return self.get_response(request)
