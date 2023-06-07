from func_call_patcher_api import hints
from func_call_patcher_api.dependency_container import __dependency_container__
from func_call_patcher_api.logic.register import FuncCallPatcherData
from func_call_patcher_api.logic.validators import validate


class CRUDService:
    """CRUD над FuncCallPatcherData"""
    @staticmethod
    def update_is_active_state(pk: hints.FuncCallPatcherId) -> None:
        __dependency_container__.func_call_patcher_data_register().change_is_active_state(pk=pk)

    @staticmethod
    def delete(pk: hints.FuncCallPatcherId) -> None:
        __dependency_container__.func_call_patcher_data_register().remove(pk=pk)

    @staticmethod
    def create_new_func_call_patcher_data(
        decorator_inner_func_as_str: hints.DecoratorInnerFuncAsStr,
        is_method: bool,
        path_to_func_in_executable_module: str,
        line_number_where_func_executed: int,
    ) -> hints.FuncCallPatcherId:

        validate(
            decorator_inner_func_as_str=decorator_inner_func_as_str,
            is_method=is_method,
            path_to_func_in_executable_module=path_to_func_in_executable_module,
            line_number_where_func_executed=line_number_where_func_executed,
        )

        func_call_patch_data = FuncCallPatcherData(
            is_active=True,
            path_to_func_in_executable_module=path_to_func_in_executable_module,
            line_number_where_func_executed=line_number_where_func_executed,
            is_method=is_method,
            decorator_inner_func_as_str=decorator_inner_func_as_str,
        )

        __dependency_container__.func_call_patcher_data_register().add(func_call_patcher_data=func_call_patch_data)
        return func_call_patch_data.pk
