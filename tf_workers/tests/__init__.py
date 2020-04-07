import unittest
import logging
import os
import os.path

from pyramid import testing
from paste.deploy import appconfig

log = logging.getLogger(__name__)

here = os.path.dirname(__file__)
if os.path.exists(os.path.join(here, '../../', 'test.ini')):
    settings = appconfig('config:' + os.path.join(here, '../../', 'test.ini'))


class TestBase(unittest.TestCase):
    "Base class for test cases (unit tests)"

    @classmethod
    def setUpClass(cls):

        cls.settings = settings

    def assert_all_in(self, keys, collection, exp_to_raise=AssertionError):
        "Assert that all given keys are present in the given collection, dict, list or tuple"

        for key in keys:
            if key not in collection:
                raise exp_to_raise

        return True

    def assert_any_in(self, keys, collection, exp_to_raise=AssertionError):
        "Assert that any of the given keys is present in the given collection, dict, list or tuple"

        for key in keys:
            if key in collection:
                return True

        raise exp_to_raise

    def assert_none_in(self, keys, collection, exp_to_raise=AssertionError):
        "Assert that none of the given keys is present in the given collection, dict, list or tuple"

        for key in keys:
            if key in collection:
                raise exp_to_raise

        return True
