from django.urls import path

from .views import FuncPatcherDetail, FuncPatchersTemplateView

urlpatterns = [
    path('', FuncPatchersTemplateView.as_view()),
    path('func_patcher_detail/', FuncPatcherDetail.as_view()),
]
