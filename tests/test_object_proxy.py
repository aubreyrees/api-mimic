import importlib
import pytest
try:
    from unittest import mock
except ImportError:
    import mock
from contextlib import contextmanager


def api():
    def funcA(a, b, c):
        pass

    def funcB(a='x', b=2, c=None):
        pass

    def funcC(a, b, c, d=None, *args, **kwargs):
        pass

    return {
        'funcA': funcA,
        'funcB': funcB,
        'funcC': funcC,
    }


@contextmanager
def mock_callback(*args, **kwargs):
    callback = mock.Mock()
    yield callback
    callback.assert_called_once_with(*args, **kwargs)


@pytest.fixture()
def full_mimic():
    module = importlib.import_module('api_mimic')
    return module.full_mimic_factory(api())


@pytest.fixture()
def shallow_mimic():
    module = importlib.import_module('api_mimic')
    return module.shallow_mimic_factory(api())


@pytest.mark.parametrize("test_args", [
    ("a", "b", "c"),
    (1, 2, 3),
])
def test_full_mimic_positonal_only(test_args, full_mimic):
    with mock_callback('funcA', test_args, {}) as callback:
        full_mimic(callback).funcA(*test_args)

@pytest.mark.parametrize("test_args,expected_kwargs", [
    ({"a": True, "b": "t", "c": 2}, (True,"t",2)),
    ({"a": 5, "b": None}, (5,None,None)),
    ({"b": False}, ("x",False,None)),
])
def test_full_mimic_only_maybe_kwargs_as_only_kwargs(test_args, expected_kwargs, full_mimic):
    with mock_callback('funcB', expected_kwargs, {}) as callback:
        full_mimic(callback).funcB(**test_args)
