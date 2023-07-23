# About

Provides factory fuctions that create classes that mimic a provided a dict
of functions (which have no return values) and invokes a callback when the
mimiced methods/functions are called.


# Installation

Supported Python versions are: 3.8, 3.9, 3.10, 3.11

To install using pip:

```
    pip install api-mimic
```

You can obtain the source from:

```
    https://github.com/aubreyrees/api-mimic
```

# Usage

`api_mimic.make_mimic_factory(api_dict)`

This function takes a dictionary of string/function key/value pairs
and uses them to create a factory function. The function values in the
dictionary should not have return values. The factroy function takes a
callback function as its sole argument and it returns a class whose methods
match the names and function signatures of the dictionary keys & function
values signatures.

This callback function takes a string and a dictionary as it's
positional arguments. This function is called when a method of the
generated class is invoked. The name of the method called is used as
the callback function's first argument, and the arguments that the
method was invoked with as the second.

The method's arguments are passed as a dictionary with the argument name
as the key for that argument's value. If the method can be invoked with
unbound positional arguments (e.g. \*args) then the argument name and a 
tuple of all unbound arguments form a key pair.

# Example usage

```
    In [1]: from api_mimic import mimic_factory
       ...:
       ...: def func1(a, b, c):
       ...:     pass
       ...:
       ...:
       ...: def func2(a, *b, c, **kwargs):
       ...:     pass
       ...:
       ...:
       ...: def callback(name, args):
       ...:   print('function name: ' + name)
       ...:   print('function called with: ' + str(args))
       ...:
       ...:
       ...: factory = make_mimic_factory({'func1': func1, 'func2': func2})
       ...:
       ...: factory(callback).func2(1, 2, 3, 4, 5, c=6, d=7)
    
    Out[1]: function name: func2
       ...: function called with: {'a': 1, 'b': (2, 3, 4, 5), 'c': 6, 'd': 7}
```
 
# Build Tools

The git repo has various tools for development.

## Scripts

Utility scripts are found in the `scripts` directory in the repository's root.

`scripts/make_venv.sh` builds a virtual enviorment for development tools in the
repository root directory.

`source scripts/activate.sh` is a shorthand to activate the development 
virtual enviroment and fails gracefully if the enviroment has not been
build.

`scripts/safe_bin.sh` will run a binary in the 
virtual enviroment's bin directory and fail gracefully if the
enviroment has not been build. For example:

```
scripts/safe_bin.sh python -m pip install build
```

Will use the Python binary in the virtual enviroment's binary
directory and pass all further arguments to the binary.

## Makefile

A Makefile is included with targets for common development tasks.
Runt `make help` to see these. Of note our `make tox` to run tests
in using `tox` and `make build` which runs tests using `tox` and 
if all tests pass builds the pacakage.

# Authors
Aubrey Rees <aubrey@kleetope.net>

# Copyright

Copyright © Aubrey Rees <aubrey@kleetope.net>


# License
api-mimic is licensed under the GPL3. See
LICENSE for the full license.
