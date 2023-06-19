from func_call_patcher.validators import BaseValidatationException

from func_call_patcher_api.service.crud_service import CRUDService

from mock import Mock, patch

import pytest


@pytest.fixture(scope='function')
def base_template_page_url(django_setup) -> str:
    from django.urls import reverse

    return reverse(viewname='base_template_page')


@pytest.fixture(scope='function')
def func_patcher_detail_url(django_setup) -> str:
    from django.urls import reverse

    return reverse(viewname='func_patcher_detail')


class TestFuncPatcherTemplateView:
    def test_key_in_context_data_exists(self, django_setup: None, base_template_page_url: str):
        from rest_framework.test import APIRequestFactory

        from func_call_patcher_api.endpoint.django_api.views import FuncPatcherTemplateView

        factory = APIRequestFactory()
        request = factory.get(base_template_page_url)

        view = FuncPatcherTemplateView()
        view.setup(request=request)

        context_data = view.get_context_data()

        patchers_data = context_data.get('patchers_data', None)
        assert patchers_data is not None


class TestFuncPatcherDetailApiView:
    @patch.object(CRUDService, 'update_is_active_state')
    def test_put_200(
        self,
        mock_crud_service__update_is_active_state: Mock,
        django_setup: None,
        func_patcher_detail_url: str,
    ):
        from rest_framework.test import APIRequestFactory

        from func_call_patcher_api.endpoint.django_api.views import FuncPatcherDetailApiView

        mock_crud_service__update_is_active_state.return_value = None
        factory = APIRequestFactory()
        data = {'func_patcher_pk': '1'}
        request = factory.put(path=func_patcher_detail_url, data=data, format='json')
        response = FuncPatcherDetailApiView.as_view()(request)

        assert response.status_code == 200
        mock_crud_service__update_is_active_state.assert_called_once_with(pk=1)

    @patch.object(CRUDService, 'update_is_active_state')
    def test_put_400(
        self,
        mock_crud_service__update_is_active_state: Mock,
        django_setup: None,
        func_patcher_detail_url: str,
    ):
        from rest_framework.test import APIRequestFactory

        from func_call_patcher_api.endpoint.django_api.views import FuncPatcherDetailApiView

        mock_crud_service__update_is_active_state.side_effect = BaseValidatationException('text of exception')
        factory = APIRequestFactory()
        data = {'func_patcher_pk': '1'}
        request = factory.put(path=func_patcher_detail_url, data=data, format='json')
        response = FuncPatcherDetailApiView.as_view()(request)

        assert response.status_code == 400
        assert response.data == {'exception': 'text of exception'}
        mock_crud_service__update_is_active_state.assert_called_once_with(pk=1)

    @patch.object(CRUDService, 'delete')
    def test_delete(
        self,
        mock_crud_service__delete: Mock,
        django_setup: None,
        func_patcher_detail_url: str,
    ):
        from rest_framework.test import APIRequestFactory

        from func_call_patcher_api.endpoint.django_api.views import FuncPatcherDetailApiView

        mock_crud_service__delete.return_value = None
        factory = APIRequestFactory()
        data = {'func_patcher_pk': '1'}
        request = factory.delete(path=func_patcher_detail_url, data=data, format='json')
        response = FuncPatcherDetailApiView.as_view()(request)

        assert response.status_code == 200
        mock_crud_service__delete.assert_called_once_with(pk=1)

    @patch.object(CRUDService, 'create_new_func_call_patcher_data')
    def test_post_status_200(
        self,
        mock_crud_service__create_new_func_call_patcher_data: Mock,
        django_setup: None,
        func_patcher_detail_url: str,
    ):
        from rest_framework.test import APIRequestFactory

        from func_call_patcher_api.endpoint.django_api.views import FuncPatcherDetailApiView

        factory = APIRequestFactory()

        data = {
            'decorator_inner_func': 'decorator_inner_func',
            'is_method': True,
            'path_to_func': 'path_to_func',
            'executable_module_name': 'executable_module_name',
            'line_number_where_func_executed': '10',
        }

        request = factory.post(func_patcher_detail_url, data=data, format='json')
        mock_crud_service__create_new_func_call_patcher_data.return_value = 1
        response = FuncPatcherDetailApiView.as_view()(request)
        assert response.status_code == 200
        assert response.data == {'created_patch_data_pk': 1}

        mock_crud_service__create_new_func_call_patcher_data.assert_called_once_with(
            decorator_inner_func_as_str='decorator_inner_func',
            is_method=True,
            path_to_func='path_to_func',
            executable_module_name='executable_module_name',
            line_number_where_func_executed=10,
        )

    @patch.object(CRUDService, 'create_new_func_call_patcher_data')
    def test_post_status_400(
        self,
        mock_crud_service__create_new_func_call_patcher_data: Mock,
        django_setup: None,
        func_patcher_detail_url: str,
    ):
        from rest_framework.test import APIRequestFactory

        from func_call_patcher_api.endpoint.django_api.views import FuncPatcherDetailApiView

        factory = APIRequestFactory()

        data = {
            'decorator_inner_func': 'decorator_inner_func',
            'is_method': True,
            'path_to_func': 'path_to_func',
            'executable_module_name': 'executable_module_name',
            'line_number_where_func_executed': '10',
        }

        request = factory.post(func_patcher_detail_url, data=data, format='json')
        mock_crud_service__create_new_func_call_patcher_data.side_effect = BaseValidatationException(
            'text of exception',
        )
        response = FuncPatcherDetailApiView.as_view()(request)
        assert response.status_code == 400
        assert response.data == {'exception': 'text of exception'}
