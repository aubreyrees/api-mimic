=====
About
=====

This modules provides functionality to create classes with the intention
of mimicking another module or classes API and then invoking a dispatch
function to implement some desired, alternate behaviour.


Installation
============

Supported Python versions are: 2.7, 3.4 and 3.5.

To install using pip:

::

    pip install api-mimic

You can obtain the source from:

::

    https://github.com/aubreyrees/api-mimic


Usage
=====

``api_mimic.make_mimic_factory(api_dict)``

This function takes a dictionary of string/function key/value pairs
and uses them to create a factory function. This function takes a
callback function as its sole argument and it returns a class whose methods
exactly match the names and function signatures of those in the dictionary.

This callback function takes a string and a dictionary as it's
positional arguments. This function is called when a method of the
generated class is invoked. The name of the method called is used as
the callback function's first argument, and the arguments that the
method was invoked with as the second.

The method's arguments are passed as a dictionary with the argument name
as the key for that argument's value. If the method can be invoked with
unbound positional arguments (e.g. \*args) then the argument name and a 
tuple of all unbound arguments form a key pair.

Example usage
=============

::

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

 
Testing
=======

``tox`` is used to run the tests. First clone
the git repository and then enter the cloned repository:

::

    git clone https://github.com/aubreystarktoller/api-mimic
    cd api-mimic

And invoke `tox`

Other Test Utils
----------------

``make`` is used for various maintence & testing tasks.

``make 
``make lint`` lints the code


Authors
=======
* Aubrey Rees <aubrey@kleetope.net>


License
=======
api-mimic is licensed under the GPL3. See
LICENSE for the full license.
