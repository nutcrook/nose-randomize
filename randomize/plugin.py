"""
This plugin randomizes the order of tests within a unittest.TestCase class

The original source of the code is:

http://code.google.com/p/python-nose/issues/detail?id=255

and the original author is: Charles McCreary

"""
__test__ = False

import logging
from nose.plugins import Plugin
from nose import loader
from inspect import isfunction, ismethod
from nose.case import FunctionTestCase, MethodTestCase
from nose.core import TextTestRunner
from nose.failure import Failure
from nose.util import isclass, isgenerator, transplant_func, transplant_class
import random
import unittest
import os

log = logging.getLogger(__name__)


class Randomize(Plugin):
    """
    Randomize the order of the tests within a unittest.TestCase class
    """
    name = 'randomize'
    # Generate a seed for deterministic behaviour
    seed = random.getrandbits(32)
    stopOnError = False

    def options(self, parser, env):
        """Register commandline options.
        """
        Plugin.options(self, parser, env)
        parser.add_option('--randomize', action='store_true', dest='randomize',
                          help="Randomize the order of the tests within a unittest.TestCase class")
        parser.add_option('--seed', action='store', dest='seed', default=None, type=long,
                          help="Initialize the seed for deterministic behavior in reproducing failed tests")

    def configure(self, options, config):
        """
        Configure plugin.
        """
        Plugin.configure(self, options, config)
        self.config = config
        self.classes_to_look_at = []
        if options.randomize:
            self.enabled = True
            if options.seed is not None:
                self.seed = options.seed
            random.seed(self.seed)
            print("Using %d as seed" % (self.seed,))
        if options.stopOnError:
            self.stopOnError = True
        self.enabled = True

    def loadTestsFromNames(self, names, module=None):
        pass

    def wantClass(self, cls):
        self.classes_to_look_at.append(cls)
        #Change this to populate a list that makeTest can then process?

    def makeTest(self, obj, parent=None):
        """Given a test object and its parent, return a test case
        or test suite.
        """
        self.ldr = loader.TestLoader()
        if isinstance(obj, unittest.TestCase):
            return obj
        elif isclass(obj):
            if parent and obj.__module__ != parent.__name__:
                obj = transplant_class(obj, parent.__name__)
            if issubclass(obj, unittest.TestCase):
                # Randomize the order of the tests in the TestCase
                return self.randomized_loadTestsFromTestCase(obj)
            else:
                return self.randomized_loadTestsFromTestClass(obj)
        elif ismethod(obj):
            if parent is None:
                parent = obj.__class__
            if issubclass(parent, unittest.TestCase):
                return parent(obj.__name__)
            else:
                if isgenerator(obj):
                    return self.ldr.loadTestsFromGeneratorMethod(obj, parent)
                else:
                    return MethodTestCase(obj)
        elif isfunction(obj):
            if parent and obj.__module__ != parent.__name__:
                obj = transplant_func(obj, parent.__name__)
            if isgenerator(obj):
                return self.ldr.loadTestsFromGenerator(obj, parent)
            else:
                return [FunctionTestCase(obj)]
        else:
            return Failure(TypeError,
                           "Can't make a test from %s" % obj)

    def randomized_loadTestsFromTestClass(self, cls):
        tests = loader.TestLoader().loadTestsFromTestClass(cls)
        return self._shuffler(tests)

    def randomized_loadTestsFromContextSuite(self, suite):
        tests = loader.TestLoader().loadTestsFromTestModule(suite)
        return self._shuffler(tests)

    def randomized_loadTestsFromTestCase(self, testCaseClass):
        tests = loader.TestLoader().loadTestsFromTestCase(testCaseClass)
        return self._shuffler(tests)

    def _shuffler(self, tests):
        """Shuffles the given tests"""
        randomized_tests = []
        for t in tests._tests:
            randomized_tests.append(t)
        random.shuffle(randomized_tests)
        tests._tests = (t for t in randomized_tests)
        return tests
    
    def addError(self, test, err):
        """Enter pdb if configured to debug errors.
        """
        print("addError!!!")
        if not self.enabled_for_errors:
            return
        self.debug(err)

    def addFailure(self, test, err):
        """Enter pdb if configured to debug failures.
        """
        print("addFailure!")
        if not self.enabled_for_failures:
            return
        self.debug(err)

    # def wasSuccessful(self, **kw):
    #     pass

    # def prepareTestRunner(self, runner):
    #     print("Going to run my own tests.")
    #     return RandomizeTestRunner(stream=runner.stream,
    #         verbosity=self.config.verbosity,
    #         config=self.config,
    #         loaderClass=self.ldr)


class RandomizeTestRunner(TextTestRunner):
    def __init__(self, **kw):
        self.loaderClass = kw.pop('loaderClass', loader.defaultTestLoader)
        super(RandomizeTestRunner, self).__init__(**kw)

    def run(self, test):
        print("Config: %s" % str(self.config))

    def wasSuccessful(self, **kw):
        pass

