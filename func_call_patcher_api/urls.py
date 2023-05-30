from django.conf.urls import url

from .views import FuncPatcherDetail, FuncPatchersTemplateView

urlpatterns = [
    url(r'^func_patcher_detail/$', FuncPatcherDetail.as_view()),
    url(r'', FuncPatchersTemplateView.as_view()),
]
