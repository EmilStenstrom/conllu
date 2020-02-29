# coding: utf-8
from __future__ import unicode_literals

import unittest
from collections import OrderedDict
from textwrap import dedent

from conllu.compat import string_to_file
from conllu.models import TokenList
from conllu.parser import (
    DEFAULT_FIELDS, ParseException, head_to_token, parse_comment_line, parse_conllu_plus_fields, parse_dict_value,
    parse_id_value, parse_int_value, parse_line, parse_nullable_value, parse_paired_list_value, parse_sentences,
    parse_token_and_metadata, serialize, serialize_field,
)


class TestParseConlluPlusFields(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(parse_conllu_plus_fields(string_to_file("")), None)
        self.assertEqual(parse_conllu_plus_fields(string_to_file(None)), None)

    def test_simple(self):
        data = dedent("""\
            # global.columns = ID FORM UPOS HEAD DEPREL MISC PARSEME:MWE
            1\tDer\tDET\t2\tdet\t_\t*
        """)
        self.assertEqual(
            parse_conllu_plus_fields(string_to_file(data)),
            ["id", "form", "upos", "head", "deprel", "misc", "parseme:mwe"]
        )

    def test_empty_columns(self):
        data = dedent("""\
            # global.columns =
            1\tDer\tDET\t2\tdet\t_\t*
        """)
        self.assertEqual(parse_conllu_plus_fields(string_to_file(data)), None)

class TestParseSentencesGenerator(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(list(parse_sentences(string_to_file(""))), [])
        self.assertEqual(list(parse_sentences(string_to_file(None))), [])

    def test_simple(self):
        data = dedent("""\
            1\thej
            2\tdå
            3\thej

            1\thej
            2\tdå
            3\thej
        """)
        sentences = list(parse_sentences(string_to_file(data)))
        self.assertEqual(sentences, [
            '1\thej\n2\tdå\n3\thej',
            '1\thej\n2\tdå\n3\thej',
        ])

    def test_multiple_newlines(self):
        data = dedent("""\
            1\thej
            2\tdå


            1\thej
            2\tdå



            1\thej
            2\tdå
        """)
        sentences = list(parse_sentences(string_to_file(data)))
        self.assertEqual(sentences, [
            '1\thej\n2\tdå',
            '1\thej\n2\tdå',
            '1\thej\n2\tdå',
        ])

    def test_ends_without_newline(self):
        data = "1\thej\n2\tdå"
        sentences = list(parse_sentences(string_to_file(data)))
        self.assertEqual(sentences, [
            '1\thej\n2\tdå',
        ])

class TestParseTokenAndMetadata(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ParseException):
            parse_token_and_metadata(None)

    def test_newlines_in_sentence(self):
        data = dedent("""\
            # meta = data
            1\thej
            2\tdå

            3\thej
            4\tdå
        """)
        tokens, metadata = parse_token_and_metadata(data)
        self.assertListEqual(tokens, [
            OrderedDict([("id", 1), ("form", "hej")]),
            OrderedDict([("id", 2), ("form", "då")]),
            OrderedDict([("id", 3), ("form", "hej")]),
            OrderedDict([("id", 4), ("form", "då")]),
        ])
        self.assertEqual(metadata, OrderedDict([("meta", "data")]))

    def test_invalid_metadata(self):
        data = dedent("""\
            # meta = data2
            # meta = data
            # newdoc
            # newpar
            # meta
            # = data
        """)
        _, metadata = parse_token_and_metadata(data)
        self.assertEqual(metadata, OrderedDict([
            ("meta", "data"),
            ("newdoc", None),
            ("newpar", None),
        ]))

    def test_custom_metadata_parsers(self):
        data = dedent("""\
            # global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
            # newdoc id = mf920901-001
            # newpar id = mf920901-001-p1
            # sent_id = mf920901-001-p1s1A
            # text = Slovenská ústava: pro i proti
            # text_en = Slovak constitution: pros and cons
        """)
        _, metadata = parse_token_and_metadata(data)
        self.assertEqual(metadata, OrderedDict([
            ("global.columns", "ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC"),
            ("newdoc id", "mf920901-001"),
            ("newpar id", "mf920901-001-p1"),
            ("sent_id", "mf920901-001-p1s1A"),
            ("text", "Slovenská ústava: pro i proti"),
            ("text_en", "Slovak constitution: pros and cons"),
        ]))

        _, metadata = parse_token_and_metadata(
            data,
            metadata_parsers={"global.columns": lambda key, value: (key, value.split())}
        )
        self.assertEqual(metadata, OrderedDict([
            ("global.columns", ["ID", "FORM", "LEMMA", "UPOS", "XPOS", "FEATS", "HEAD", "DEPREL", "DEPS", "MISC"]),
            ("newdoc id", "mf920901-001"),
            ("newpar id", "mf920901-001-p1"),
            ("sent_id", "mf920901-001-p1s1A"),
            ("text", "Slovenská ústava: pro i proti"),
            ("text_en", "Slovak constitution: pros and cons"),
        ]))

    def test_one_to_many_custom_metadata_parser(self):
        data = dedent("""\
            #\tid='1'-document_id='36:1047'-span='1'
        """)

        _, metadata = parse_token_and_metadata(
            data,
            metadata_parsers={
                "id": lambda key, value: [
                    (pair.split("=", 1)[0], pair.split("=", 1)[1].strip("'"))
                    for pair in (key + "=" + value).split("-")
                ]
            },
        )
        self.assertEqual(metadata, OrderedDict([
            ("id", "1"),
            ("document_id", "36:1047"),
            ("span", "1"),
        ]))

    def test_fallback_metadata_parser(self):
        data = dedent("""\
            #20191005
        """)

        _, metadata = parse_token_and_metadata(
            data,
            metadata_parsers={
                "__fallback__": lambda key, value: ("sentence-id", key),
            },
        )
        self.assertEqual(metadata, OrderedDict([
            ("sentence-id", "20191005"),
        ]))

    def test_custom_fields(self):
        data = dedent("""\
            1\t1\t1
            2\t2\t2
        """)
        tokens, _ = parse_token_and_metadata(data, fields=("id", "id", "id"))
        self.assertEqual(tokens, [
            OrderedDict([("id", 1), ("id", 1), ("id", 1)]),
            OrderedDict([("id", 2), ("id", 2), ("id", 2)]),
        ])

    def test_custom_field_parsers(self):
        data = dedent("""\
            1\tbackwards\tline
            2\tparis\tsirap
        """)
        fields = ("id", "backwards")

        # A field parser that takes all remaining field, reverses their letters and joins them
        def parse_backwards(value):
            return " ".join([part[::-1] for part in value])

        # This overrides the default parsers, so the id is parsed as a string
        field_parsers = {
            "id": lambda line, i: line[i],
            "backwards": lambda line, i: parse_backwards(line[i:len(line)])
        }

        tokens, _ = parse_token_and_metadata(data, fields=fields, field_parsers=field_parsers)
        self.assertEqual(tokens, [
            OrderedDict([("id", '1'), ("backwards", "sdrawkcab enil")]),
            OrderedDict([("id", '2'), ("backwards", "sirap paris")]),
        ])

    def test_default_field_parsers_when_undefined(self):
        data = dedent("""\
            1\tfrom
            2\tparis
        """)
        fields = ("id", "form")
        field_parsers = {
            # Rely on default 'id' field parser
            "form": lambda line, i: line[i].upper()
        }
        tokens, _ = parse_token_and_metadata(data, fields=fields, field_parsers=field_parsers)
        self.assertEqual(tokens, [
            OrderedDict([("id", 1), ("form", "FROM")]),
            OrderedDict([("id", 2), ("form", "PARIS")]),
        ])


class TestParseLine(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ParseException) as assert_context:
            line = "invalid_id\t_\t_\t_\t_\t_\t_\t_\t_\t"
            parse_line(line, fields=DEFAULT_FIELDS)

        expected = "Failed parsing field 'id'"
        self.assertEqual(str(assert_context.exception)[:len(expected)], expected)

    def test_parse_line(self):
        line = "1\tThe\tthe\tDET\tDT\tDefinite=Def|PronType=Art\t4\tdet\t_\t_"
        self.assertEqual(
            parse_line(line, fields=DEFAULT_FIELDS),
            OrderedDict([
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
            ])
        )

    def test_parse_line_nullable_fields(self):
        line = "_\t_\t_\t_\t_\t_\t_\t_\t_\t_"
        self.assertEqual(
            dict(parse_line(line, fields=DEFAULT_FIELDS)),
            dict([
                ('id', None),
                ('form', '_'),
                ('lemma', '_'),
                ('upostag', '_'),
                ('xpostag', None),
                ('feats', None),
                ('head', None),
                ('deprel', '_'),
                ('deps', None),
                ('misc', None)
            ])
        )

    def test_parse_line_only_id_head(self):
        line = "1\tThe\tthe\tDET\tDT\tDefinite=Def|PronType=Art\t4\tdet\t_\t_"
        self.assertEqual(parse_line(line, fields=["id", "form"]), OrderedDict([
            ('id', 1),
            ('form', 'The'),
        ]))

    def test_parse_line_fewer_columns(self):
        line = "1\tThe\tthe\tDET\tDT"
        self.assertEqual(parse_line(line, fields=DEFAULT_FIELDS), OrderedDict([
            ('id', 1),
            ('form', 'The'),
            ('lemma', 'the'),
            ('upostag', 'DET'),
            ('xpostag', 'DT'),
        ]))

    def test_parse_line_without_spacing(self):
        line = "1ThetheDETDTDefinite=Def|PronType=Art4det__"
        with self.assertRaises(ParseException) as assert_context:
            parse_line(line, fields=DEFAULT_FIELDS)

        expected = "Invalid line format"
        self.assertEqual(str(assert_context.exception)[:len(expected)], expected)

    def test_parse_line_with_spaces(self):
        line = "1 The the DET DT Definite=Def|PronType=Art 4 det _ _"
        with self.assertRaises(ParseException) as assert_context:
            parse_line(line, fields=DEFAULT_FIELDS)

        expected = "Invalid line format"
        self.assertEqual(str(assert_context.exception)[:len(expected)], expected)

    def test_parse_line_two_spaces(self):
        line = "1  The  the  DET  DT  Definite=Def|PronType=Art  4  det  _  _"
        self.assertEqual(parse_line(line, fields=["id", "form"]), OrderedDict([
            ('id', 1),
            ('form', 'The'),
        ]))

class TestParseCommentLine(unittest.TestCase):
    def test_parse_spaces_before_square(self):
        data = ["# a = 1", "  # a = 1", "\t# a = 1"]
        for item in data:
            self.assertEqual(parse_comment_line(item), [("a", "1")])

    def test_parse_comment_line(self):
        data = "# sent_id = 1"
        self.assertEqual(parse_comment_line(data), [("sent_id", "1")])

    def test_parse_comment_line_multiple_equals(self):
        data = "# text = five plus three = eight"
        self.assertEqual(parse_comment_line(data), [("text", "five plus three = eight")])

    def test_parse_comment_line_without_square(self):
        data = "sent_id = 1"
        with self.assertRaises(ParseException):
            parse_comment_line(data)

    def test_parse_comment_line_without_equals(self):
        data = "# sent_id: 1"
        self.assertEqual(parse_comment_line(data), [])

    def test_parse_comment_line_without_space(self):
        data = "#sent_id = 1"
        self.assertEqual(parse_comment_line(data), [("sent_id", "1")])

    def test_parse_comment_line_optional_value(self):
        data = '# newdoc'
        self.assertEqual(parse_comment_line(data), [("newdoc", None)])
        data = '# newpar'
        self.assertEqual(parse_comment_line(data), [("newpar", None)])
        data = '# invalid'
        self.assertEqual(parse_comment_line(data), [])

    def test_parse_comment_line_optional_value_no_space(self):
        data = '#newdoc'
        self.assertEqual(parse_comment_line(data), [("newdoc", None)])
        data = '#newpar'
        self.assertEqual(parse_comment_line(data), [("newpar", None)])
        data = '#invalid'
        self.assertEqual(parse_comment_line(data), [])


class TestParseIntValue(unittest.TestCase):
    def test_parse_int_value(self):
        self.assertEqual(parse_int_value("_"), None)
        self.assertEqual(parse_int_value("4"), 4)
        self.assertEqual(parse_int_value("0"), 0)
        self.assertEqual(parse_int_value("10"), 10)
        self.assertEqual(parse_int_value("-10"), -10)

        with self.assertRaises(ParseException):
            parse_int_value("a")

class TestParseIDValue(unittest.TestCase):
    def _run_valid_invalid_tests(self, valid, invalid=[]):
        for value, result in valid:
            self.assertEqual(parse_id_value(value), result)

        for value in invalid:
            with self.assertRaises(ParseException):
                parse_id_value(value)

    def test_none(self):
        self._run_valid_invalid_tests([
            ("_", None),
            (None, None),
        ])

    def test_single(self):
        self._run_valid_invalid_tests([
            ("4", 4),
            ("10", 10),
            ("0", 0),
        ], [
            "-10",
            "a",
        ])

    def test_range(self):
        self._run_valid_invalid_tests([
            ("1-2", (1, "-", 2)),
            ("1-999", (1, "-", 999)),
            ("1000-1001", (1000, "-", 1001)),
        ], [
            "1-1",
            "1-0",
            "0-1-2",
            "0-a",
            "a-0",
        ])

    def test_decimal(self):
        self._run_valid_invalid_tests([
            ("0.1", (0, ".", 1)),
            ("1.1", (1, ".", 1)),
            ("1.10", (1, ".", 10)),
            ("10.1", (10, ".", 1)),
        ], [
            "1.0",
            "a.0",
            "0.a",
        ])

class TestParsePairedListValue(unittest.TestCase):
    def test_parse_paired_list(self):
        self.assertEqual(
            parse_paired_list_value("4:nsubj"),
            [("nsubj", 4)]
        )
        self.assertEqual(
            parse_paired_list_value("1:under_case_:under_case_|2:dash-sign-:dash-sign-"),
            [("under_case_:under_case_", 1), ("dash-sign-:dash-sign-", 2)]
        )
        self.assertEqual(
            parse_paired_list_value("2:nsubj|4:nsubj"),
            [("nsubj", 2), ("nsubj", 4)]
        )
        self.assertEqual(
            parse_paired_list_value("1:flat:name|2:amod|20:nsubj"),
            [("flat:name", 1), ("amod", 2), ("nsubj", 20)]
        )
        self.assertEqual(
            parse_paired_list_value("5:conj:and|8.1:nsubj:pass|9:nsubj:xsubj"),
            [("conj:and", 5), ("nsubj:pass", (8, ".", 1)), ("nsubj:xsubj", 9)]
        )
        self.assertEqual(
            parse_paired_list_value("1:compound|6:ARG|9:ARG1|10:ARG2"),
            [('compound', 1), ('ARG', 6), ('ARG1', 9), ('ARG2', 10)]
        )
        self.assertNotEqual(
            parse_paired_list_value("1:compound|6:ARG|9:ARG1|10:2ARG"),
            [('compound', 1), ('ARG', 6), ('ARG1', 9), ('2ARG', 10)]
        )
        self.assertEqual(
            parse_paired_list_value("0:root"),
            [('root', 0)]
        )
        self.assertEqual(
            parse_paired_list_value("1:obl:arg:gen"),
            [('obl:arg:gen', 1)]
        )
        self.assertEqual(
            parse_paired_list_value("25:obl:arg:į"),
            [('obl:arg:į', 25)]
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
            parse_dict_value("key1"),
            OrderedDict([("key1", "")])
        )
        self.assertEqual(
            parse_dict_value("key1=val1"),
            OrderedDict([("key1", "val1")])
        )
        self.assertEqual(
            parse_dict_value("key1=val1|key2=val2"),
            OrderedDict([("key1", "val1"), ("key2", "val2")])
        )
        self.assertEqual(
            parse_dict_value("key1=val1|key2|key3=val3"),
            OrderedDict([("key1", "val1"), ("key2", ""), ("key3", "val3")])
        )
        self.assertEqual(
            parse_dict_value("key1=val1|key1=val2"),
            OrderedDict([("key1", "val2")])
        )
        self.assertEqual(
            parse_dict_value("key1=_|_|_=val1"),
            OrderedDict([("key1", None)])
        )
        self.assertEqual(parse_dict_value(""), None)
        self.assertEqual(parse_dict_value("_"), None)

class TestParseNullableValue(unittest.TestCase):
    def test_parse_nullable_value(self):
        self.assertEqual(parse_nullable_value("_"), None)
        self.assertEqual(parse_nullable_value(""), None)
        self.assertEqual(parse_nullable_value("hello"), "hello")

class TestHeadToToken(unittest.TestCase):
    maxDiff = None

    def test_simple(self):
        self.assertEqual(
            head_to_token([
                {"data": "a", "head": 0},
                {"data": "dog", "head": 1},
                {"data": "wags", "head": 2},
                {"data": "tail", "head": 1},
            ]),
            {
                0: [{"data": "a", "head": 0}],
                1: [{"data": "dog", "head": 1}, {"data": "tail", "head": 1}],
                2: [{"data": "wags", "head": 2}],
            }
        )

    def test_missing_head(self):
        with self.assertRaises(ParseException):
            head_to_token([])

        with self.assertRaises(ParseException):
            head_to_token([{"data": "a"}])

    def test_negative_head(self):
        self.assertEqual(
            head_to_token([
                {"data": "a", "head": 0},
                {"data": "dog", "head": 1},
                {"data": "wags", "head": -1},
                {"data": "tail", "head": -2},
            ]),
            {
                0: [{"data": "a", "head": 0}],
                1: [{"data": "dog", "head": 1}],
            }
        )

    def test_range_ids_ignored(self):
        self.assertEqual(
            dict(head_to_token([
                {"data": "a", "head": 0},
                {"data": "dog", "head": 1},
                {"data": "a dog", "head": 0, "id": (1, "-", 2)},  # Range node
                {"data": "wags", "head": 2},
                {"data": "tail", "head": 1},
            ])),
            {
                0: [{"data": "a", "head": 0}],
                1: [{"data": "dog", "head": 1}, {"data": "tail", "head": 1}],
                2: [{"data": "wags", "head": 2}],
            }
        )

    def test_decimal_ids_ignored(self):
        self.assertEqual(
            dict(head_to_token([
                {"data": "a", "head": 0},
                {"data": "dog", "head": 1},
                {"data": "that", "head": 1, "id": (1, ".", 1)},
                {"data": "wags", "head": 2},
                {"data": "its", "head": 2, "id": (2, ".", 1)},  # Empty node
                {"data": "tail", "head": 1},
            ])),
            {
                0: [{"data": "a", "head": 0}],
                1: [{"data": "dog", "head": 1}, {"data": "tail", "head": 1}],
                2: [{"data": "wags", "head": 2}],
            }
        )


class TestSerializeField(unittest.TestCase):
    def test_ordered_dict(self):
        data = OrderedDict()
        self.assertEqual(serialize_field(data), "")

        data = OrderedDict([('SpaceAfter', 'No')])
        self.assertEqual(serialize_field(data), "SpaceAfter=No")

        data = OrderedDict([('Translit', None)])
        self.assertEqual(serialize_field(data), "Translit=_")

    def test_none(self):
        data = None
        self.assertEqual(serialize_field(data), "_")

    def test_string(self):
        data = "ADJ"
        self.assertEqual(serialize_field(data), "ADJ")

    def test_tuple(self):
        data = (1, "-", 2)
        self.assertEqual(serialize_field(data), "1-2")

        data = (100, ".", 2)
        self.assertEqual(serialize_field(data), "100.2")

        with self.assertRaises(ParseException):
            serialize_field([(1, "-", 2)])

    def test_list(self):
        data = [("nsubj", 2), ("nmod", 1)]
        self.assertEqual(serialize_field(data), "2:nsubj|1:nmod")

class TestSerialize(unittest.TestCase):
    def test_identity_unicode(self):
        data = "5\tlängtar\n\n"
        tokenlist = TokenList(*parse_token_and_metadata(data))
        self.assertEqual(serialize(tokenlist), data)

    def test_metadata(self):
        data = dedent("""\
            # newdoc
            # data = meta
            # meta = data
            1\tdog

        """)
        tokenlist = TokenList(*parse_token_and_metadata(data))
        self.assertEqual(serialize(tokenlist), data)

    def test_serialize_tricky_fields(self):
        data = dedent("""\
            5\tjumps\tjump\tVERB\tVBZ\tMood=Ind|Number=Sing\t0\troot\t_\tSpaceAfter=No
        """)
        tokenlist = TokenList(*parse_token_and_metadata(data))
        self.assertEqual(serialize(tokenlist).strip(), data.strip())
