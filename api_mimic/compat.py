"""
Smooths out incompatibilities between different versions of Python

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
