from django.urls import path

from .views import FuncPatcherDetailApiView, FuncPatcherTemplateView

urlpatterns = [
    path('', FuncPatcherTemplateView.as_view(), name='base_template_page'),
    path('func_patcher_detail/', FuncPatcherDetailApiView.as_view(), name='func_patcher_detail'),
]
