import unittest
from conllu.parser import parse, parse_tree
from tests.fixtures.data1 import data1


class TestIntegration(unittest.TestCase):
    def test_parse(self):
        from tests.fixtures.data1_flat import data1_expected
        self.assertEqual(
            list(list(x) for x in parse(data1)), data1_expected)

    def test_parse_tree(self):
        from tests.fixtures.data1_tree import data1_expected
        self.assertEqual(
            next(parse_tree(data1)), data1_expected)
