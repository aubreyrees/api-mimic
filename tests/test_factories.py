import pytest
import itertools
from pytest import local as l


@pytest.mark.parametrize("test_args,test_kwargs", list(itertools.product(
    (
        tuple(),
        ("f", 32),
        ("x", 5, True, "y"),
        (5, "y", "j", False, "7", "i"),
    ),
    (
        {},
        {"a":"x", "b":5, "c":True, "d":"y"},
        {"a":None, "b":77},
        {"c":52, "d":"x"},
        {"a":"g", "b":None, "c":"6f", "d":5, "e": 5, "f":"q"},
    )))
)
def test_my_test(mimic, singleton_api, test_args, test_kwargs):
    func_name = next(iter(singleton_api))
    sig = singleton_api[func_name].sig
    cls = mimic(singleton_api)

    extra = sum(1 for k in test_kwargs.keys() if l.NAMES.index(k) < sig.args)

    if (
        # to few args
        sig.args > (len(test_args) + extra) or
        # to many args
        (not sig.unbound_args and sig.arg_count() < (len(test_args) + extra)) or
        # to many kwargs
        (not sig.unbound_kwargs and (sig.all_args_count()) < len(test_kwargs)) or
        # arg provided using both parg and kwarg
        (test_kwargs and any(l.NAMES.index(k) < min(sig.arg_count(), len(test_args)) for k in test_kwargs.keys())) or
        # values provided for non-existant kwargs
        (not sig.unbound_kwargs and any(l.NAMES.index(k) >= sig.all_args_count() for k in test_kwargs.keys())) or
        # required kwargs are missing
        (sig.kwargs != 0 and len(set(l.NAMES[sig.arg_count():sig.arg_count() + sig.kwargs]).difference(test_kwargs.keys())) > 0)
    ):
        with pytest.raises(TypeError):
            getattr(cls(l.null_func), func_name)(*test_args, **test_kwargs)

    else:
        expected_args = test_args
        expected_kwargs = {}
        additional = []

        for name, value in test_kwargs.items():
            idx = l.NAMES.index(name)
            if idx <= sig.arg_count():
                additional.append((idx, value))
            else:
                expected_kwargs[name] = value

        expected_args += tuple(x[1] for x in sorted(additional, key=lambda t: t[0]))

        callback = l.mock.Mock()
        getattr(cls(callback), func_name)(*test_args, **test_kwargs)

        callback.called_once_with(func_name, expected_args, expected_kwargs)
