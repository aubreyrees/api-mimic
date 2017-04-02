"""
Smooths out incompatibilities between different versions of Python
"""

# pylint: disable=import-error,invalid-name

import sys


__all__ = ('signature', 'Parameter')


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY2:
    import funcsigs
    signature = funcsigs.signature
    Parameter = funcsigs.Parameter
elif PY3:
    import inspect
    signature = inspect.signature
    Parameter = inspect.Parameter
