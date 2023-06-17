from func_call_patcher_api.logic.func_call_patcher_data import FuncCallPatcherData
from func_call_patcher_api.logic.register import InMemoryFuncCallPatcherDataRegister
from func_call_patcher_api.service import crud_service
from func_call_patcher_api.service.crud_service import CRUDService

from mock import Mock, patch


class TestCRUDService:
    def test_update_is_active_state(
        self,
        mock_func_patcher_data_register: InMemoryFuncCallPatcherDataRegister,
        func_patcher_test_data: FuncCallPatcherData,
    ):
        PK = 1
        mock_func_patcher_data_register._data = {PK: func_patcher_test_data}

        assert mock_func_patcher_data_register.data[PK].is_active is True
        CRUDService.update_is_active_state(pk=PK)
        assert mock_func_patcher_data_register.data[PK].is_active is False

    def test_delete(
        self,
        mock_func_patcher_data_register: InMemoryFuncCallPatcherDataRegister,
        func_patcher_test_data: FuncCallPatcherData,
    ):
        PK = 1
        mock_func_patcher_data_register._data = {PK: func_patcher_test_data}

        assert mock_func_patcher_data_register.data.get(PK, None)
        CRUDService.delete(pk=PK)
        assert mock_func_patcher_data_register.data.get(PK, None) is None

    @patch.object(crud_service, 'validate')
    def test_create_new_func_call_patcher_data(
        self,
        mock_validate: Mock,
        mock_func_patcher_data_register: InMemoryFuncCallPatcherDataRegister,
    ):
        assert mock_func_patcher_data_register.data == {}
        pk_of_created_record = CRUDService.create_new_func_call_patcher_data(
            decorator_inner_func_as_str='decorator_inner_func_as_str',
            is_method=True,
            path_to_func='path_to_func',
            executable_module_name='executable_module_name',
            line_number_where_func_executed=10,
        )
        mock_validate.assert_called_once_with(
            decorator_inner_func_as_str='decorator_inner_func_as_str',
            is_method=True,
            path_to_func='path_to_func',
            executable_module_name='executable_module_name',
            line_number_where_func_executed=10,
        )
        assert pk_of_created_record == 1
        created_func_call_patcher_data = mock_func_patcher_data_register.data.get(pk_of_created_record, None)
        assert created_func_call_patcher_data is not None
        assert created_func_call_patcher_data.is_active is True
        assert created_func_call_patcher_data.path_to_func == 'path_to_func'
        assert created_func_call_patcher_data.executable_module_name == 'executable_module_name'
        assert created_func_call_patcher_data.line_number_where_func_executed == 10
        assert created_func_call_patcher_data.is_method is True
        assert created_func_call_patcher_data.decorator_inner_func_as_str == 'decorator_inner_func_as_str'
