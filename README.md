nose-randomize
==============

A plugin to allow nose to run tests in a random order

## About
When nose runs the tests in a given project, the order that the tests are loaded and excuted is always the same.

For unit tests, an ideal situation is one of isolation: Each test should be able to run independently of the other tests in the project. If there is a dependency (such as test_A must run first in order for test_B to pass) then the test authors might want to look into how their tests are setup.

This plugin allows for randomization of the tests in a test class when they are run. In theory this should prove _(or disprove)_ the isolation of the tests because they can be run in a random order every time and this should expose any pre-condition dependencies that might exist.

## Installation

To install from source:
 * Checkout or download the source
 * cd into the directory and execute:

```shell
python setup.py install
```

To install from pip:

```shell
pip install randomize
```

## Usage

### Basic usage
The following will execute the tests and print out the seed that was used to start the random number generator. This is useful for tracking down test failures: if there is a depedency that causes a failure, re-running the test suite with the same seed should allow the failure to be repeatable.

```shell
nosetests --randomize
```

To re-run the tests with a given seed number, use this command line:

```shell
nosetests --randomize --seed=<whatever number you wish to use>
```

To only randomize selected TestCases class, use the --class-specific, and the @randomize_tests decorator.
@randomize_tests supports a predefined seed. If no seed is given, a seed will be randomly generated.

```python
# A random seed will be generated
@randomize_tests()
class MyClass(unittest.TestCase):
    pass

@randomize_tests(seed=1723930311)
class MyOtherClass(unittest.TestCase):
    pass
```

```shell
nosetests --randomize --class-specific
```

## Limitations

Currently this plugin is only able to randomize the tests within a Class or Module. It does not support running the Classes in a random order. 

For example if you have 3 test classes (TestClass1, TestClass2, TestClass3), they will be called in that order. The tests within each class will be executed in a random order, but the classes them selves will be called in the same order every time.

Moreover, options --class-specific and --seed conflict. In such scenario, Class specific randomization will be ignored, and the given seed will be used.
************

## Important notes

 * *License* - This plugin is LGPL Licensed per the original author

 * *Original author* - This work is based on the code created by nloadholtes, as posted to https://github.com/nloadholtes/nose-randomize,
 and by Charles McCreary as posted to https://code.google.com/p/python-nose/issues/detail?id=255
