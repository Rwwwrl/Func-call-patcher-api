from django.conf.urls import url

from .views import FuncPatcherDetailApiView, FuncPatcherTemplateView

urlpatterns = [
    url(r'^func_patcher_detail/$', FuncPatcherDetailApiView.as_view(), name='func_patcher_detail'),
    url(r'', FuncPatcherTemplateView.as_view(), name='base_template_page'),
]
