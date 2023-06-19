from func_call_patcher_api.dependency_container import __dependency_container__
from func_call_patcher_api.logic.func_call_patcher_data import FuncCallPatcherData
from func_call_patcher_api.logic.repository import InMemoryRepository
from func_call_patcher_api.pytests.utils import YieldFixture

import pytest


@pytest.fixture(scope='function')
def mock_func_patcher_data_register() -> YieldFixture[InMemoryRepository]:
    register = InMemoryRepository()
    override = __dependency_container__.repository_factory.override(register)
    override.__enter__()
    yield __dependency_container__.repository_factory()
    override.__exit__()


@pytest.fixture(scope='session')
def func_patcher_test_data() -> FuncCallPatcherData:
    return FuncCallPatcherData(
        is_active=True,
        path_to_func='path_to_func',
        executable_module_name='executable_module_name',
        line_number_where_func_executed=10,
        is_method=True,
        decorator_inner_func_as_str='decorator_inner_func_as_str',
    )
