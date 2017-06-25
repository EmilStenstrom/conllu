from collections import OrderedDict
import unittest
from conllu.parser import (
    parse,
    parse_tree,
    parse_line,
    parse_int_value,
    parse_dict_value,
    parse_nullable_value,
)
from tests.fixtures.data import data1
from tests.fixtures.data_flat import data1_flat
from tests.fixtures.data_tree import data1_tree

class TestParse(unittest.TestCase):
    def test_parse_data1(self):
        self.assertEqual(parse(data1), data1_flat)

    def test_parse_only_id_data1(self):
        ids = [parsed_line["id"] for parsed_line in parse(data1, fields=["id"])[0]]
        num_lines = len(data1.strip().split("\n"))
        self.assertEqual(ids, range(1, num_lines + 1))

class TestParseTree(unittest.TestCase):
    def test_parse_tree(self):
        self.assertEqual(parse_tree(data1), data1_tree)

class TestParseLine(unittest.TestCase):
    def test_parse_line(self):
        line = "1\tThe\tthe\tDET\tDT\tDefinite=Def|PronType=Art\t4\tdet\t_\t_"
        self.assertEqual(parse_line(line), OrderedDict([
            ('id', 1),
            ('form', 'The'),
            ('lemma', 'the'),
            ('upostag', 'DET'),
            ('xpostag', 'DT'),
            ('feats', OrderedDict([('Definite', 'Def'), ('PronType', 'Art')])),
            ('head', 4),
            ('deprel', 'det'),
            ('deps', None),
            ('misc', None)
        ]))

    def test_parse_line_only_id_head(self):
        line = "1\tThe\tthe\tDET\tDT\tDefinite=Def|PronType=Art\t4\tdet\t_\t_"
        self.assertEqual(parse_line(line, fields=["id", "form"]), OrderedDict([
            ('id', 1),
            ('form', 'The'),
        ]))

class TestParseIntValue(unittest.TestCase):
    def test_parse_int_value(self):
        self.assertEqual(parse_int_value("4"), 4)
        self.assertEqual(parse_int_value("0"), 0)
        self.assertEqual(parse_int_value("10"), 10)
        self.assertEqual(parse_int_value("-10"), None)
        self.assertEqual(parse_int_value("a"), None)

class TestParseDictValue(unittest.TestCase):
    def test_parse_dict_value(self):
        self.assertEqual(
            parse_dict_value("key1=val1"),
            OrderedDict([("key1", "val1")])
        )
        self.assertEqual(
            parse_dict_value("key1=val1|key2=val2"),
            OrderedDict([("key1", "val1"), ("key2", "val2")])
        )
        self.assertEqual(parse_dict_value(""), None)
        self.assertEqual(parse_dict_value("_"), None)

class TestParseNullableValue(unittest.TestCase):
    def test_parse_nullable_value(self):
        self.assertEqual(parse_nullable_value("_"), None)
        self.assertEqual(parse_nullable_value(""), None)
        self.assertEqual(parse_nullable_value("hello"), "hello")
