from typing import Any, Dict

from django.views.generic import TemplateView

from func_call_patcher.validators import BaseValidatationException

from func_call_patcher_api.dependency_container import __dependency_container__
from func_call_patcher_api.service.crud_service import CRUDService

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class FuncPatcherTemplateView(TemplateView):
    template_name = 'django_api/index.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data()
        context_data['patchers_data'] = __dependency_container__.repository_factory().all
        return context_data


class FuncPatcherDetailApiView(APIView):
    def put(self, request):
        CRUDService.update_is_active_state(pk=int(request.data['func_patcher_pk']))
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        CRUDService.delete(pk=int(request.data['func_patcher_pk']))
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def _bad_request_response(error_text: str) -> Response:
        return Response({'exception': error_text}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        decorator_inner_func_as_str = request.data['decorator_inner_func']
        is_method = request.data['is_method']
        path_to_func = request.data['path_to_func']
        executable_module_name = request.data['executable_module_name']
        try:
            line_number_where_func_executed = int(request.data['line_number_where_func_executed'])
        except ValueError:
            self._bad_request_response(
                error_text=f"""
                line where func executed должен быть int, вы передали:
                {line_number_where_func_executed.__class__.__name__}
                """,
            )

        try:
            created_patch_data_pk = CRUDService.create_new_func_call_patcher_data(
                decorator_inner_func_as_str=decorator_inner_func_as_str,
                is_method=is_method,
                path_to_func=path_to_func,
                executable_module_name=executable_module_name,
                line_number_where_func_executed=line_number_where_func_executed,
            )
        except BaseValidatationException as e:
            return self._bad_request_response(str(e))
        else:
            return Response({'created_patch_data_pk': created_patch_data_pk}, status=status.HTTP_200_OK)
