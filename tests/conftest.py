import pytest
import itertools
import importlib
import sys
import random
try:
    from collections import UserDict
except ImportError:
    from UserDict import IterableUserDict as UserDict
try:
    from unittest import mock
except ImportError:
    import mock



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
            s.append('{}: {}'.format(name, func.code.strip()))
        return '{' + ', '.join(s) + '}'



class Sig:
    UNBOUND_ARG_NAME = 'args'
    UNBOUND_KWARG_NAME = 'kwargs'

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


def make_func(sig):
    scaffold = {}
    code = 'def func({sig}): pass\n'.format(sig=sig)
    exec(code, scaffold)
    func = scaffold['func']
    func.sig = sig
    func.code = code
    return func


def make_api(*sigs):
    return API(("func" + str(idx), make_func(sig)) for idx, sig in enumerate(sigs))


def null_func(*args, **kwargs):
    pass


def sig_permutations():
    params = itertools.product(range(3), range(3), (False, True), range(3), range(3), (False, True))

    for param in params:
        res = Sig(*param)
        if sys.version_info < (3,3) and (param[3] != 0 or param[4] != 0):
            res = pytest.mark.skip(res, reason="keyword only arguments don't exist before Python 3")

        yield res


########################################################################
##
## FIXTURES 
##
########################################################################


@pytest.fixture(params=list(sig_permutations()))
def signature(request):
    return request.param


@pytest.fixture()
def singleton_api(signature):
    return make_api(signature)


@pytest.fixture()
def mimic():
    module = importlib.import_module('api_mimic')
    return module.mimic_factory


########################################################################
##
## HOOKS
##
########################################################################



def pytest_namespace():
    return {
        'local': type('LocalPytest', (object,), {
            'mock': mock,
            'null_func': null_func,
            'NAMES': NAMES,
            'DEFAULTS': DEFAULTS,
        })
    }
