import unittest
from conllu.parser import parse
from tests.fixtures.data1 import data1

class TestIntegration(unittest.TestCase):
    def test_parse(self):
        from tests.fixtures.data1_flat import data1_expected
        self.assertEqual(parse(data1), data1_expected)
