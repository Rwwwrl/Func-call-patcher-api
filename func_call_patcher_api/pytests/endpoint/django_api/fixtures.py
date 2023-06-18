import os

import django

from func_call_patcher_api.pytests.utils import YieldFixture

import pytest


@pytest.fixture(scope='function')
def django_setup() -> YieldFixture[None]:
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'func_call_patcher_api.pytests.endpoint.django_api.test_settings',
    )
    django.setup()
    yield
    del os.environ['DJANGO_SETTINGS_MODULE']
