import importlib
import inspect


def module_to_api(module_name, use_all=True, ignore_private=True, exclude=None):
    module = importlib.import_module(module_name)

    if use_all:
        members =  module.__all__
    elif ignore_private:
        members = (m for m in dir(module) if not m.startsswith('_'))

    if exclude:
        members = (m for m in members if m not in exclude)

    return {m: getattr(module, m) for m in members}


def iface_init(self, callback):
    self.callback = callback


def full_mimic_factory(target):
    attrs = {'__init__': iface_init}

    for op_func_name, op_func in target.items():
        op_func_sig = inspect.signature(op_func)

        arg_names = []
        kwarg_names = []
        unbound_args = None
        unbound_kwargs = None
        proxy_op_func_str_args = "self"

        for param in op_func_sig.parameters.values():
            proxy_op_func_str_args += ', ' + str(param)

            if (
                param.kind == inspect.Parameter.POSITIONAL_ONLY or
                param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            ):
                arg_names.append(param.name)
            elif param.kind == inspect.Parameter.VAR_POSITIONAL:
                unbound_args = param.name
            elif param.kind == inspect.Parameter.KEYWORD_ONLY:
                kwarg_names.append(param.name)
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                unbound_kwargs = param.name

        func_body = []

        func_body.append('saved_args = [' + ', '.join(arg_names) + ']')
        if unbound_args is not None:
            func_body[-1] += ' + ' + unbound_args

        func_body.append('saved_kwargs = {' + ', '.join('"{0}": {0}'.format(n) for n in kwarg_names) + '}')
        if unbound_kwargs is not None:
            func_body.append('saved_kwargs.update({})'.format(unbound_kwargs))

        func_body.append('return self.callback("{}", tuple(saved_args), saved_kwargs)'.format(op_func_name))

        code = "def {}({}):\n    {}\n".format(op_func_name, proxy_op_func_str_args, '\n    '.join(func_body))
        exec(code, attrs)

    return type('Proxy', (object,), attrs)


def shallow_mimic_factory(target, sig):
    attrs = {'__init__': iface_init}

    params = ', '.join(str(p) for p in sig.parameters.values()[2:])
    tpl = "def {{0}}(self, {0}):\n    self.callback(\"{{0}}\", {0})\n".format(params)

    for op_func_name in target.keys():
        exec(tpl.format(op_func_name), attrs)

    return type('Interface', (object,), attrs)
