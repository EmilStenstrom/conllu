import unittest
from collections import OrderedDict

from conllu.parser import (
    ParseException, parse, parse_dict_value, parse_int_value, parse_line, parse_nullable_value,
    parse_paired_list_value, parse_tree, serialize_tree,
)

from tests.fixtures.data import data1, data2, data3, data4, data5, data6, data7, data8
from tests.fixtures.data_flat import data1_flat, data2_flat, data3_flat, data4_flat, data6_flat
from tests.fixtures.data_tree import data1_tree, data5_tree, data6_tree


class TestParse(unittest.TestCase):
    def test_parse_data1(self):
        self.assertEqual(parse(data1), data1_flat)

    def test_parse_only_id_data1(self):
        ids = [parsed_line["id"] for parsed_line in parse(data1, fields=["id"])[0]]
        num_lines = len(data1.strip().split("\n"))
        self.assertEqual(ids, list(range(1, num_lines + 1)))

    def test_parse_data2(self):
        self.assertEqual(parse(data2), data2_flat)

    def test_parse_data3(self):
        self.assertEqual(parse(data3), data3_flat)

    def test_parse_data4(self):
        self.assertEqual(parse(data4), data4_flat)

    def test_parse_data6(self):
        self.assertEqual(parse(data6), data6_flat)

    def test_parse_data7(self):
        parse(data7)

class TestParseTree(unittest.TestCase):
    def test_parse_tree(self):
        test_cases = zip([data1, data5, data6],
                         [data1_tree, data5_tree, data6_tree])
        for data, data_tree in test_cases:
            self.assertEqual(parse_tree(data), data_tree)

    def test_parse_data8(self):
        parse_tree(data8)

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

    def test_parse_line_with_no_tabs(self):
        line = "1 The the DET DT Definite=Def|PronType=Art 4 det _ _"
        with self.assertRaises(ParseException):
            parse_line(line)

    def test_parse_line_two_spaces(self):
        line = "1  The  the  DET  DT  Definite=Def|PronType=Art  4  det  _  _"
        self.assertEqual(parse_line(line, fields=["id", "form"]), OrderedDict([
            ('id', 1),
            ('form', 'The'),
        ]))

class TestParseIntValue(unittest.TestCase):
    def test_parse_int_value(self):
        self.assertEqual(parse_int_value("4"), 4)
        self.assertEqual(parse_int_value("0"), 0)
        self.assertEqual(parse_int_value("10"), 10)
        self.assertEqual(parse_int_value("-10"), -10)
        self.assertEqual(parse_int_value("a"), None)

class TestParsePairedListValue(unittest.TestCase):
    def test_parse_paired_list(self):
        self.assertEqual(
            parse_paired_list_value("4:nsubj"),
            [("nsubj", 4)]
        )
        self.assertEqual(
            parse_paired_list_value("0:under_case_:under_case_|1:dash-sign-:dash-sign-"),
            [("under_case_:under_case_", 0), ("dash-sign-:dash-sign-", 1)]
        )
        self.assertEqual(
            parse_paired_list_value("2:nsubj|4:nsubj"),
            [("nsubj", 2), ("nsubj", 4)]
        )
        self.assertEqual(
            parse_paired_list_value("0:flat:name|1:amod|20:nsubj"),
            [("flat:name", 0), ("amod", 1), ("nsubj", 20)]
        )

    def test_parse_empty(self):
        testcases = [
            "",
            "_",
        ]
        for testcase in testcases:
            # Empty strings should return None
            self.assertEqual(parse_paired_list_value(testcase), None)

    def test_parse_invalid(self):
        testcases = [
            "x:nsubj",
            "0:",
            "0:_",
            "0:-",
            ":",
            ":nsubj",
            "1:nsubj|",
            "1:nsubj||1:nsubj",
        ]
        for testcase in testcases:
            # Invalid strings should be returned untouched
            self.assertEqual(parse_paired_list_value(testcase), testcase)

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

class TestSerialize(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(serialize_tree(data1_tree[0]), data1.strip())

    def test_identity_unicode(self):
        self.assertEqual(serialize_tree(data5_tree[0]), data5.strip())
