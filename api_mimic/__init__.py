"""
This modules provides functionality to create classes with the intention
of mimicking another module or classes API and then invoking a dispatch
function to implement some desired, alternate behaviour.

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


from .factories import mimic_factory


__all__ = ['mimic_factory']
