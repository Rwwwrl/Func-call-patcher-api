from func_call_patcher_api.logic.register import InMemoryFuncCallPatcherDataRegister
from func_call_patcher_api.logic.value_objects import FuncCallPatcherData
from func_call_patcher_api.service import crud_service
from func_call_patcher_api.service.crud_service import CRUDService

from mock import Mock, patch


class TestCRUDService:
    def test_update_is_active_state(
        self,
        mock_func_patcher_data_register: InMemoryFuncCallPatcherDataRegister,
        func_patcher_test_data: FuncCallPatcherData,
    ):
        mock_func_patcher_data_register._data = {func_patcher_test_data.pk: func_patcher_test_data}

        assert mock_func_patcher_data_register.data[func_patcher_test_data.pk].is_active is True
        CRUDService.update_is_active_state(pk=func_patcher_test_data.pk)
        assert mock_func_patcher_data_register.data[func_patcher_test_data.pk].is_active is False

    def test_delete(
        self,
        mock_func_patcher_data_register: InMemoryFuncCallPatcherDataRegister,
        func_patcher_test_data: FuncCallPatcherData,
    ):
        mock_func_patcher_data_register._data = {func_patcher_test_data.pk: func_patcher_test_data}

        assert mock_func_patcher_data_register.data.get(func_patcher_test_data.pk, None)
        CRUDService.delete(pk=func_patcher_test_data.pk)
        assert mock_func_patcher_data_register.data.get(func_patcher_test_data.pk, None) is None

    @patch.object(crud_service, 'validate')
    def test_create_new_func_call_patcher_data(
        self,
        mock_validate: Mock,
        mock_func_patcher_data_register: InMemoryFuncCallPatcherDataRegister,
    ):
        assert mock_func_patcher_data_register.data == {}
        CRUDService.create_new_func_call_patcher_data(
            decorator_inner_func_as_str='decorator_inner_func_as_str',
            is_method=True,
            path_to_func_in_executable_module='path_to_func_in_executable_module',
            line_number_where_func_executed=10,
        )
        mock_validate.assert_called_once_with(
            decorator_inner_func_as_str='decorator_inner_func_as_str',
            is_method=True,
            path_to_func_in_executable_module='path_to_func_in_executable_module',
            line_number_where_func_executed=10,
        )
        new_func_call_patcher_data = mock_func_patcher_data_register.data.get(1, None)
        assert new_func_call_patcher_data is not None
        assert new_func_call_patcher_data.pk == 1
        assert new_func_call_patcher_data.is_active is True
        assert new_func_call_patcher_data.path_to_func_in_executable_module == 'path_to_func_in_executable_module'
        assert new_func_call_patcher_data.line_number_where_func_executed == 10
        assert new_func_call_patcher_data.is_method is True
        assert new_func_call_patcher_data.decorator_inner_func_as_str == 'decorator_inner_func_as_str'
