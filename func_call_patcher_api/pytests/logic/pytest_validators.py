from func_call_patcher import validators as func_call_patcher_validators

from func_call_patcher_api.logic.validators import (
    DecoratorInnerFuncIncorrectValidator,
    DecoratorInnerFuncIsIncorrect,
    validate,
)

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


class TestValidate:
    @patch.object(DecoratorInnerFuncIncorrectValidator, '__init__')
    @patch.object(DecoratorInnerFuncIncorrectValidator, 'validate')
    @patch.object(func_call_patcher_validators, 'validate')
    def test(
        self,
        mock_validate_mock: Mock,
        mock_DecoratorInnerFuncIncorrectValidator_validate: Mock,
        mock_DecoratorInnerFuncIncorrectValidator_init: Mock,
    ):
        mock_DecoratorInnerFuncIncorrectValidator_init.return_value = None
        validate(
            decorator_inner_func_as_str='decorator_inner_func_as_str',
            is_method=True,
            path_to_func='path_to_func',
            executable_module_name='executable_module_name',
            line_number_where_func_executed=10,
        )
        mock_validate_mock.assert_called_once_with(
            line_number_where_func_executed=10,
            path_to_func='path_to_func',
            executable_module_name='executable_module_name',
            is_method=True,
        )
        mock_DecoratorInnerFuncIncorrectValidator_init.assert_called_once_with(obj='decorator_inner_func_as_str')
        mock_DecoratorInnerFuncIncorrectValidator_validate.assert_called_once()
