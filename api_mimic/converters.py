import importlib


def module_to_api(module_name, use_all=True, ignore_private=True, exclude=None):
    module = importlib.import_module(module_name)

    if use_all:
        members = module.__all__
    elif ignore_private:
        members = (m for m in dir(module) if not m.startsswith('_'))

    if exclude:
        members = (m for m in members if m not in exclude)

    return {m: getattr(module, m) for m in members}
