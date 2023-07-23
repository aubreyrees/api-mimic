"""
Functions for mimicing & repurposing functions without return values.

Provides factory fuctions that create classes that mimic a provided a dict
of functions (which have no return values) and invokes a callback when the
mimiced methods/functions are called.

api-mimic is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

api-mimic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with api-mimic.  If not, see <http://www.gnu.org/licenses/>.
"""

import inspect
from typing import Dict, Callable, Any


__all__ = ['make_mimic_factory']


def mimic_factory(target : Dict[str, Callable[..., Any]]) \
            -> Callable[[Callable[[str, Dict], None]], type]:
    """Decprecated function - use `make_mimic_factory`."""
    from warnings import warn
    warn('This is deprecated', DeprecationWarning, stacklevel=2)
    return make_mimic_factory(target)


def make_mimic_factory(target : Dict[str, Callable[..., Any]]) \
            -> Callable[[Callable[[str, dict], None]], type]:
    """
    Create a factory that produces a mimic class.

    The factory function takes a callback as an argument and produces
    a class whose interface mimics target and then invokes the provided
    callback when the mimiced function is called.
    """
    code = "def factory(callback):"

    for op_func_name, op_func in target.items():
        op_func_sig = inspect.signature(op_func)

        names = []
        unbound_kwargs = None
        unbound_args = None
        kwargs_seen = False
        proxy_op_func_str_args = "self"

        for param in op_func_sig.parameters.values():
            if (
                    param.kind == inspect.Parameter.POSITIONAL_ONLY or
                    param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            ):
                names.append(param.name)
            elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                unbound_args = True
                names.append(param.name)
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                unbound_kwargs = param.name
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                if not unbound_args and not kwargs_seen:
                    proxy_op_func_str_args += ',*'
                kwargs_seen = True
                names.append(param.name)
            else:  # pragma: no cover
                raise Exception("Unknown parameter type (change to python core?)")

            proxy_op_func_str_args += ',' + str(param)


        args = ', '.join('"{0}": {0}'.format(n) for n in names)
        func_body = f'args = {{{args}}}'

        if unbound_kwargs is not None:
            func_body += f'\n            args.update({unbound_kwargs})'

        code += f"""
    def {op_func_name}_factory(cb):
        def func({proxy_op_func_str_args}):
            {func_body}
            return cb("{op_func_name}", args)
        return func
"""

    code += "\n    attrs = {\n"
    for op_func_name in target.keys():
        code += f'        "{op_func_name}": {op_func_name}_factory(callback),\n'
    code += "    }\n"
    code += "    return type('Proxy', (object,), attrs)()"

    attrs = {}
    exec(code, None, attrs)
    return attrs['factory']
