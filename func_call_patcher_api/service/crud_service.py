from func_call_patcher_api import hints
from func_call_patcher_api.dependency_container import __dependency_container__
from func_call_patcher_api.logic.repository import FuncCallPatcherData
from func_call_patcher_api.logic.validators import validate


class CRUDService:
    """CRUD над FuncCallPatcherData"""
    @staticmethod
    def update_is_active_state(pk: hints.FuncCallPatcherId) -> None:
        repository = __dependency_container__.repository_factory()
        record = repository.get(pk=pk)
        if not record.is_active:
            # в случае если мы меняем с неактивного статуса на активный, то
            # нужно провалидировать не является ли патч на эту функцию активным в другой записи
            validate(
                decorator_inner_func_as_str=record.decorator_inner_func_as_str,
                is_method=record.is_method,
                path_to_func=record.path_to_func,
                executable_module_name=record.executable_module_name,
                line_number_where_func_executed=record.line_number_where_func_executed,
            )
        repository.change_active_state_to_opposite(pk=pk)

    @staticmethod
    def delete(pk: hints.FuncCallPatcherId) -> None:
        __dependency_container__.repository_factory().delete(pk=pk)

    @staticmethod
    def create_new_func_call_patcher_data(
        decorator_inner_func_as_str: hints.DecoratorInnerFuncAsStr,
        is_method: bool,
        path_to_func: str,
        executable_module_name: str,
        line_number_where_func_executed: int,
    ) -> hints.FuncCallPatcherId:

        validate(
            decorator_inner_func_as_str=decorator_inner_func_as_str,
            is_method=is_method,
            path_to_func=path_to_func,
            executable_module_name=executable_module_name,
            line_number_where_func_executed=line_number_where_func_executed,
        )

        func_call_patch_data = FuncCallPatcherData(
            is_active=True,
            path_to_func=path_to_func,
            executable_module_name=executable_module_name,
            line_number_where_func_executed=line_number_where_func_executed,
            is_method=is_method,
            decorator_inner_func_as_str=decorator_inner_func_as_str,
        )

        pk_of_created_record = __dependency_container__.repository_factory().add(
            func_call_patcher_data=func_call_patch_data,
        )
        return pk_of_created_record
