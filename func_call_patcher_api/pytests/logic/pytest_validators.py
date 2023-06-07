from func_call_patcher import validators as func_call_patcher_validators

from func_call_patcher_api.logic.register import InMemoryFuncCallPatcherDataRegister
from func_call_patcher_api.logic.validators import (
    DecoratorInnerFuncIncorrectValidator,
    DecoratorInnerFuncIsIncorrect,
    FuncPathIsDuplicatedException,
    FuncPathIsDuplicatedValidator,
    validate,
)
from func_call_patcher_api.logic.value_objects import FuncCallPatcherData

from mock import Mock, patch

import pytest


@pytest.fixture(scope='session')
def valid_decorator_inner_func_as_str() -> str:
    return """def blabla(func, func_args, func_kwargs, frame,  relationship_identifier):
        print(func_args, func_kwargs)
        return func(*func_args, **func_kwargs)
    """


@pytest.fixture(scope='session')
def invalid_decorator_inner_func_as_str() -> str:
    return """def blabla(func, func_args, func_kwargs, frame,  relationship_identifier):"""


class TestDecoratorInnerFuncIncorrectValidator:
    def test_valid(self, valid_decorator_inner_func_as_str: str):
        DecoratorInnerFuncIncorrectValidator(valid_decorator_inner_func_as_str).validate()

    def test_invalid(self, invalid_decorator_inner_func_as_str: str):
        with pytest.raises(DecoratorInnerFuncIsIncorrect):
            DecoratorInnerFuncIncorrectValidator(invalid_decorator_inner_func_as_str).validate()


class TestFuncPathIsDuplicatedValidator:
    def test_with_no_duplicates(
        self,
        mock_func_patcher_data_register: InMemoryFuncCallPatcherDataRegister,
        func_patcher_test_data: FuncCallPatcherData,
    ):
        assert mock_func_patcher_data_register.data == {}
        FuncPathIsDuplicatedValidator(func_patcher_test_data.path_to_func_in_executable_module).validate()

    def test_with_duplicates(
        self,
        mock_func_patcher_data_register: InMemoryFuncCallPatcherDataRegister,
        func_patcher_test_data: FuncCallPatcherData,
    ):
        mock_func_patcher_data_register.add(func_call_patcher_data=func_patcher_test_data)
        with pytest.raises(FuncPathIsDuplicatedException):
            FuncPathIsDuplicatedValidator(func_patcher_test_data.path_to_func_in_executable_module).validate()


class TestValidate:
    @patch.object(DecoratorInnerFuncIncorrectValidator, '__init__')
    @patch.object(FuncPathIsDuplicatedValidator, '__init__')
    @patch.object(DecoratorInnerFuncIncorrectValidator, 'validate')
    @patch.object(FuncPathIsDuplicatedValidator, 'validate')
    @patch.object(func_call_patcher_validators, 'validate')
    def test(
        self,
        mock_validate_mock: Mock,
        mock_FuncPathIsDuplicatedValidator_validate: Mock,
        mock_DecoratorInnerFuncIncorrectValidator_validate: Mock,
        mock_FuncPathIsDuplicatedValidator_init: Mock,
        mock_DecoratorInnerFuncIncorrectValidator_init: Mock,
    ):
        mock_DecoratorInnerFuncIncorrectValidator_init.return_value = None
        mock_FuncPathIsDuplicatedValidator_init.return_value = None

        validate(
            decorator_inner_func_as_str='decorator_inner_func_as_str',
            is_method=True,
            path_to_func_in_executable_module='path_to_func_in_executable_module',
            line_number_where_func_executed=10,
        )
        mock_validate_mock.assert_called_once_with(
            line_number_where_func_executed=10,
            path_to_func_in_executable_module='path_to_func_in_executable_module',
            is_method=True,
        )
        mock_DecoratorInnerFuncIncorrectValidator_init.assert_called_once_with(obj='decorator_inner_func_as_str')
        mock_FuncPathIsDuplicatedValidator_init.assert_called_once_with(obj='path_to_func_in_executable_module')
        mock_FuncPathIsDuplicatedValidator_validate.assert_called_once()
        mock_DecoratorInnerFuncIncorrectValidator_validate.assert_called_once()
