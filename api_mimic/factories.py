from . import compat


def iface_init(self, callback):
    self.callback = callback


def full_mimic_factory(target):
    attrs = {'__init__': iface_init}

    for op_func_name, op_func in target.items():
        op_func_sig = compat.signature(op_func)

        arg_names = []
        kwarg_names = []
        unbound_args = None
        unbound_kwargs = None
        kwargs_seen = False
        proxy_op_func_str_args = "self"

        for param in op_func_sig.parameters.values():
            if (
                    param.kind == compat.Parameter.POSITIONAL_ONLY or
                    param.kind == compat.Parameter.POSITIONAL_OR_KEYWORD
            ):
                arg_names.append(param.name)
            elif param.kind == compat.Parameter.VAR_POSITIONAL:
                unbound_args = param.name
            elif param.kind == compat.Parameter.VAR_KEYWORD:
                unbound_kwargs = param.name
            # must come last or we'll choke on python < 3
            elif param.kind == compat.Parameter.KEYWORD_ONLY:
                if not unbound_args and not kwargs_seen:
                    proxy_op_func_str_args += ',*'
                kwargs_seen = True
                kwarg_names.append(param.name)

            proxy_op_func_str_args += ',' + str(param)

        func_body = []

        func_body.append('saved_args = [' + ', '.join(arg_names) + ']')
        if unbound_args is not None:
            func_body.append('saved_args.extend(' + unbound_args + ')')

        func_body.append(
            'saved_kwargs = {{{0}}}'
            .format(', '.join('"{0}": {0}'.format(n) for n in kwarg_names))
        )
        if unbound_kwargs is not None:
            func_body.append('saved_kwargs.update({})'.format(unbound_kwargs))

        func_body.append(
            'return self.callback("{}", tuple(saved_args), saved_kwargs)'
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

        try:
            exec(code, None, attrs)
        except:
            raise Exception(code)

    return type('Proxy', (object,), attrs)


def shallow_mimic_factory(target, sig):
    attrs = {'__init__': iface_init}

    params = ', '.join(str(p) for p in sig.parameters.values()[2:])
    tpl = "def {{0}}(self, {0}):\n    self.callback(\"{{0}}\", {0})\n".format(params)

    for op_func_name in target.keys():
        exec(tpl.format(op_func_name), {}, attrs)

    return type('Interface', (object,), attrs)
