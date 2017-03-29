import itertools
import sys
import importlib
import pytest
import random
try:
    from collections import UserDict
except ImportError:
    from UserDict import IterableUserDict as UserDict
try:
    from unittest import mock
except ImportError:
    import mock
from contextlib import contextmanager

NAMES = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
DEFAULTS = ('"x"', True, None, 2, '"22"', '"aa"', (1,2,3,'"a"'), None, 2, 45, False, '"x"', '"2"', '"5a"')


class API(UserDict):
    def __str__(self):
        s = []
        for name, func in self.items():
            s.append(name + ':' + func.code)
        return '{' + ', '.join(s) + '}'

    def __repr__(self):
        s = []
        for name, func in self.items():
            s.append('{}: ({}, {}, {}, {}, {}, {})[{}]'.format(
                name,
                func.sig.args,  func.sig.args_with_default, func.sig.unbound_args,
                func.sig.kwargs,  func.sig.kwargs_with_default, func.sig.unbound_kwargs,
                func.code.strip()
            ))
        return '{' + ', '.join(s) + '}'
 
 

class Sig:
    def __init__(self, args, args_with_default, unbound_args, kwargs, kwargs_with_default, unbound_kwargs):
        self.args = args
        self.args_with_default = args_with_default
        self.unbound_args = unbound_args
        self.kwargs = kwargs
        self.kwargs_with_default = kwargs_with_default
        self.unbound_kwargs = unbound_kwargs
        self._str = None

    def arg_count(self):
        return self.args + self.args_with_default

    def kwarg_count(self):
        return self.kwargs + self.kwargs_with_default

    def all_args_count(self):
        return self.kwargs + self.kwargs_with_default + self.args + self.args_with_default

    def __str__(self):
        if self._str is None:
            seed = []
            args = []
            kwargs = []
            names = iter(NAMES)
            defaults = iter(DEFAULTS)

            for _ in range(self.args):
                label = next(names)
                args.append(label)
                seed.append(label)

            for _ in range(self.args_with_default):
                arg = next(names) + '=' + str(next(defaults))
                args.append(arg)
                seed.append(arg)

            if self.unbound_args:
                seed.append('*args')

            for _ in range(self.kwargs):
                label = next(names)
                kwargs.append(label)
                seed.append(label)

            for _ in range(self.kwargs_with_default):
                arg =  next(names) + '=' + str(next(defaults))
                kwargs.append(arg)
                seed.append(arg)

            if self.unbound_kwargs:
                seed.append('**kwargs')

            if kwargs:
                seed = ','.join(seed)
                random.seed(seed)
                random.shuffle(kwargs)

            sig = args

            if self.unbound_args:
                sig.append('*args')

            if kwargs:
                if not self.unbound_args:
                    sig.append('*')
                sig.extend(kwargs)

            if self.unbound_kwargs:
                sig.append('**kwargs')

            self._str = ",".join(sig)

        return self._str

    def __repr__(self):
        return 'Sig({}, {}, {}, {}, {}, {})'.format(
            self.args,
            self.args_with_default,
            self.unbound_args,
            self.kwargs,
            self.kwargs_with_default,
            self.unbound_kwargs
        )


def make_api(*sigs):
    final = {}
    attrs = API()
    for idx, sig in enumerate(sigs):
        func_name = "func" + str(idx)
        code = 'def {0}({1}): pass\n'.format(func_name, sig)
        try:
            exec(code, final, attrs)
        except SyntaxError:
            raise Exception(sig)
        attrs[func_name].sig = sig
        attrs[func_name].code = code
    return attrs


def null_func(*args, **kwargs):
    pass


def _sig_permutations():
    params = itertools.product(range(3), range(3), (False, True), range(3), range(3), (False, True))

    for param in params:
        res = Sig(*param)
        if sys.version_info < (3,3) and (param[3] != 0 or param[4] != 0):
            res = pytest.mark.skip(res, reason="keyword only arguments don't exist before Python 3")

        yield res


@pytest.fixture(scope="module", params=list(_sig_permutations()))
def singleton_api(request):
    return make_api(request.param)


@pytest.fixture()
def full_mimic():
    module = importlib.import_module('api_mimic')
    return module.full_mimic_factory


@pytest.fixture()
def shallow_mimic():
    module = importlib.import_module('api_mimic')
    return module.shallow_mimic_factory


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
def test_my_test(full_mimic, singleton_api, test_args, test_kwargs):
    func_name = next(iter(singleton_api))
    sig = singleton_api[func_name].sig
    cls = full_mimic(singleton_api)

    extra = sum(1 for k in test_kwargs.keys() if NAMES.index(k) < sig.args)

    if (
        # to few args
        sig.args > (len(test_args) + extra) or
        # to many args
        (not sig.unbound_args and sig.arg_count() < (len(test_args) + extra)) or
        # to many kwargs
        (not sig.unbound_kwargs and (sig.all_args_count()) < len(test_kwargs)) or
        # arg provided using both parg and kwarg
        (test_kwargs and any(NAMES.index(k) < min(sig.arg_count(), len(test_args)) for k in test_kwargs.keys())) or
        # values provided for non-existant kwargs
        (not sig.unbound_kwargs and any(NAMES.index(k) >= sig.all_args_count() for k in test_kwargs.keys())) or
        # required kwargs are missing
        (sig.kwargs != 0 and len(set(NAMES[sig.arg_count():sig.arg_count() + sig.kwargs]).difference(test_kwargs.keys())) > 0)
    ):
        with pytest.raises(TypeError):
            getattr(cls(null_func), func_name)(*test_args, **test_kwargs)

    else:
        expected_args = test_args
        expected_kwargs = {}
        additional = []

        for name, value in test_kwargs.items():
            idx = NAMES.index(name)
            if idx <= sig.arg_count():
                additional.append((idx, value))
            else:
                expected_kwargs[name] = value

        expected_args += tuple(x[1] for x in sorted(additional, key=lambda t: t[0]))

        callback = mock.Mock()
        getattr(cls(callback), func_name)(*test_args, **test_kwargs)

        callback.called_once_with(func_name, expected_args, expected_kwargs)
