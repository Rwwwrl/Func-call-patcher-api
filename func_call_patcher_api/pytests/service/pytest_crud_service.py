from func_call_patcher_api.logic.func_call_patcher_data import FuncCallPatcherData
from func_call_patcher_api.logic.repository import InMemoryRepository
from func_call_patcher_api.service import crud_service
from func_call_patcher_api.service.crud_service import CRUDService

from mock import Mock, patch


class TestCRUDService:
    @patch.object(crud_service, 'validate')
    def test_update_is_active_state(
        self,
        mock_validate: Mock,
        mock_func_patcher_data_register: InMemoryRepository,
        func_patcher_test_data: FuncCallPatcherData,
    ):
        PK = 1
        mock_validate.return_value = None

        mock_func_patcher_data_register._data = {PK: func_patcher_test_data}

        assert mock_func_patcher_data_register.all[PK].is_active is True
        CRUDService.update_is_active_state(pk=PK)
        mock_validate.assert_not_called()
        assert mock_func_patcher_data_register.all[PK].is_active is False

        CRUDService.update_is_active_state(pk=PK)
        mock_validate.assert_called_once_with(
            path_to_func='path_to_func',
            executable_module_name='executable_module_name',
            line_number_where_func_executed=10,
            is_method=True,
            decorator_inner_func_as_str='decorator_inner_func_as_str',
        )

    def test_delete(
        self,
        mock_func_patcher_data_register: InMemoryRepository,
        func_patcher_test_data: FuncCallPatcherData,
    ):
        PK = 1
        mock_func_patcher_data_register._data = {PK: func_patcher_test_data}

        assert mock_func_patcher_data_register.all.get(PK, None)
        CRUDService.delete(pk=PK)
        assert mock_func_patcher_data_register.all.get(PK, None) is None

    @patch.object(crud_service, 'validate')
    def test_create_new_func_call_patcher_data(
        self,
        mock_validate: Mock,
        mock_func_patcher_data_register: InMemoryRepository,
    ):
        assert mock_func_patcher_data_register.all == {}
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
        created_func_call_patcher_data = mock_func_patcher_data_register.all.get(pk_of_created_record, None)
        assert created_func_call_patcher_data is not None
        assert created_func_call_patcher_data.is_active is True
        assert created_func_call_patcher_data.path_to_func == 'path_to_func'
        assert created_func_call_patcher_data.executable_module_name == 'executable_module_name'
        assert created_func_call_patcher_data.line_number_where_func_executed == 10
        assert created_func_call_patcher_data.is_method is True
        assert created_func_call_patcher_data.decorator_inner_func_as_str == 'decorator_inner_func_as_str'
