from typing import List

from func_call_patcher import FuncCallPatcher, MultiFuncCallPatcher

from func_call_patcher_api.dependency_container import __dependency_container__
from func_call_patcher_api.logic.utils import FuncAsObjectFromStringGetter


class FuncCallPatcherMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        patchers: List[FuncCallPatcher] = []

        relationship_identifier = hash(request)
        for func_call_patcher_data in __dependency_container__.repository_factory().active.values():
            decorator_inner_func = FuncAsObjectFromStringGetter.exec(
                func_as_str=func_call_patcher_data.decorator_inner_func_as_str,
            )
            patchers.append(
                FuncCallPatcher(
                    path_to_func=func_call_patcher_data.path_to_func,
                    executable_module_name=func_call_patcher_data.executable_module_name,
                    line_number_where_func_executed=func_call_patcher_data.line_number_where_func_executed,
                    decorator_inner_func=decorator_inner_func,
                    is_method=func_call_patcher_data.is_method,
                    relationship_identifier=relationship_identifier,
                ),
            )

        with MultiFuncCallPatcher(*patchers):
            return self.get_response(request)
