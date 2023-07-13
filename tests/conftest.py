import importlib
import pytest
from unittest.mock import Mock


import api_mimic


def null_callback(*p, **k):
    pass


@pytest.fixture()
def api_with_null_callback():
    def f(api):
        factory = api_mimic.make_mimic_factory(api)
        return factory(null_callback)


@pytest.fixture()
def api_with_mock_callback():
    def f(api):
        mock_callback = Mock()
        factory = api_mimic.make_mimic_factory(api)
        return factory(mock_callback), mock_callback
    return f


@pytest.fixture()
def test_func():
    def inner(a, b, c):
        pass
    return inner
