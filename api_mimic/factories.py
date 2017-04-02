"""
Factories that create classes that mimic APIs

This file is part of api-mimic.

api-mimic is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

api-mimic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""


from . import compat


def iface_init(self, callback):
    """
    __init__ fuction for our generated classes
    """
    self.callback = callback


def mimic_factory(target):
    """
    Creates a class whose methods match the names and signatures of the
    functions in `target`.
    """


    attrs = {'__init__': iface_init}

    for op_func_name, op_func in target.items():
        op_func_sig = compat.signature(op_func)

        names = []
        unbound_kwargs = None
        unbound_args = None
        kwargs_seen = False
        proxy_op_func_str_args = "self"

        for param in op_func_sig.parameters.values():
            if (
                    param.kind == compat.Parameter.POSITIONAL_ONLY or
                    param.kind == compat.Parameter.POSITIONAL_OR_KEYWORD
            ):
                names.append(param.name)
            elif param.kind == compat.Parameter.VAR_POSITIONAL:
                unbound_args = True
                names.append(param.name)
            elif param.kind == compat.Parameter.VAR_KEYWORD:
                unbound_kwargs = param.name
            else:
                # param.kind == compat.Parameter.KEYWORD_ONLY
                # this is last otherwise this chokes with Python < 3
                if not unbound_args and not kwargs_seen:
                    proxy_op_func_str_args += ',*'
                kwargs_seen = True
                names.append(param.name)

            proxy_op_func_str_args += ',' + str(param)

        func_body = []


        func_body.append(
            'args = {{{0}}}'
            .format(', '.join('"{0}": {0}'.format(n) for n in names))
        )
        if unbound_kwargs is not None:
            func_body.append('args.update({})'.format(unbound_kwargs))

        func_body.append(
            'return self.callback("{}", args)'
            .format(op_func_name)
        )

        code = (
            "def {}({}):\n    {}\n"
            .format(
                op_func_name,
                proxy_op_func_str_args,
                '\n    '.join(func_body)
            )
        )

        exec(code, None, attrs)

    return type('Proxy', (object,), attrs)
