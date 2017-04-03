import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


tests_require = ['pytest', 'pytest-cov']
install_requires = []

if sys.version_info < (3,3):
    tests_require.append('mock')
    install_requires.append('funcsigs')


description = """
This modules provides functionality to create classes with the intention
of mimicking another module or classes API and then invoking a dispatch
function to implement some desired, alternate behaviour.
"""


setup(
    name='api-mimic',
    version='1.0b2',
    description='API mimicry',
    long_description=description,
    author='Aubrey Stark-Toller',
    author_email='aubrey@kleetope.uk',
    license='GPL3',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=['api_mimic'],
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass = {'test': PyTest},
)
