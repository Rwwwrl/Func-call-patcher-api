from django.urls import path

from .views import FuncPatcherDetail, FuncPatcherTemplateView

urlpatterns = [
    path('', FuncPatcherTemplateView.as_view()),
    path('func_patcher_detail/', FuncPatcherDetail.as_view()),
]
