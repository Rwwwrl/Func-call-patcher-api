from typing import Any, Dict

from django.views.generic import TemplateView

from func_call_patcher.validators import BaseValidatationException

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .func_call_patcher.register import FuncCallPatcherData, __func_call_patcher_register__
from .func_call_patcher.validators import validate


class FuncPatchersTemplateView(TemplateView):
    template_name = 'func_call_patcher_api/index.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data()
        context_data['patchers_data'] = __func_call_patcher_register__.data
        return context_data


class FuncPatcherDetail(APIView):
    def put(self, request):
        __func_call_patcher_register__.change_is_active_state(pk=int(request.data["func_patcher_pk"]))
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        __func_call_patcher_register__.remove(pk=int(request.data["func_patcher_pk"]))
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def _bad_request_response(error_text: str) -> Response:
        return Response({'exception': error_text}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        decorator_inner_func_as_str = request.data['decorator_inner_func']
        is_method = request.data['is_method']
        path_to_func_in_executable_module = request.data['path_to_func_in_executable_module']
        line_number_where_func_executed = request.data['line_number_where_func_executed']

        try:
            line_number_where_func_executed = int(line_number_where_func_executed)
        except ValueError:
            return self._bad_request_response(
                error_text=f"""
                line where func executed должен быть int, вы передали:
                {line_number_where_func_executed.__class__.__name__}
                """,
            )

        try:
            validate(
                decorator_inner_func_as_str=decorator_inner_func_as_str,
                is_method=is_method,
                path_to_func_in_executable_module=path_to_func_in_executable_module,
                line_number_where_func_executed=line_number_where_func_executed,
            )
        except BaseValidatationException as e:
            return self._bad_request_response(error_text=str(e))

        line_number_where_func_executed = int(line_number_where_func_executed)
        func_call_patch_data = FuncCallPatcherData(
            is_active=True,
            path_to_func_in_executable_module=path_to_func_in_executable_module,
            line_number_where_func_executed=line_number_where_func_executed,
            is_method=is_method,
            decorator_inner_func_as_str=decorator_inner_func_as_str,
        )

        new_patch_pk = __func_call_patcher_register__.add(func_call_patcher_data=func_call_patch_data)
        return Response({'new_patch_pk': new_patch_pk}, status=status.HTTP_200_OK)
