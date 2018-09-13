# coding: utf-8
from __future__ import unicode_literals

import sys
import unittest
from collections import OrderedDict
from textwrap import dedent

from conllu.compat import capture_print
from conllu.models import TokenList, TokenTree
from conllu.parser import ParseException, serialize


class TestTokenList(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(ParseException):
            TokenList({"id": 1})

    def test_eq(self):
        metadata = {"meta": "data"}

        tokenlist1 = TokenList([{"id": 1}])
        tokenlist1.metadata = metadata
        tokenlist2 = TokenList([{"id": 1}])
        self.assertNotEqual(tokenlist1, tokenlist2)

        tokenlist2.metadata = metadata
        self.assertEqual(tokenlist1, tokenlist2)

    def test_len(self):
        tokenlist = TokenList([{"id": 1}, {"id": 2}, {"id": 3}])
        self.assertEqual(3, len(tokenlist))

    def test_sizeof(self):
        tokenlist1 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}])
        self.assertGreater(sys.getsizeof(tokenlist1), sys.getsizeof([{"id": 1}, {"id": 2}, {"id": 3}]))

        tokenlist2 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}], {"meta": "data"})
        self.assertLess(sys.getsizeof(tokenlist1), sys.getsizeof(tokenlist2))

    def test_clear(self):
        tokenlist = TokenList([{"id": 1}, {"id": 2}, {"id": 3}], {"meta": "data"})
        tokenlist.clear()
        self.assertEqual(len(tokenlist.tokens), 0)
        self.assertEqual(tokenlist.metadata, None)

    def test_copy(self):
        tokenlist1 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}], {"meta": "data"})
        tokenlist2 = tokenlist1.copy()
        self.assertIsNot(tokenlist1, tokenlist2)
        self.assertEqual(tokenlist1, tokenlist2)

    def test_extend(self):
        tokenlist1 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}])
        tokenlist2 = [{"id": 4}, {"id": 5}, {"id": 6}]
        tokenlist1.extend(tokenlist2)
        tokenlist3 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}])
        self.assertEqual(tokenlist1, tokenlist3)

        tokenlist4 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}], {"meta1": "data1"})
        tokenlist5 = TokenList([{"id": 4}, {"id": 5}, {"id": 6}], {"meta2": "data2"})
        tokenlist4.extend(tokenlist5)
        tokenlist6 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}],
                               {"meta1": "data1", "meta2": "data2"})
        self.assertEqual(tokenlist4, tokenlist6)

        tokenlist7 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}], "abc")
        tokenlist8 = TokenList([{"id": 4}, {"id": 5}, {"id": 6}], "de")
        tokenlist7.extend(tokenlist8)
        tokenlist9 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}], "abcde")
        self.assertEqual(tokenlist7, tokenlist9)

        tokenlist7 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}], "abc")
        tokenlist8 = TokenList([{"id": 4}, {"id": 5}, {"id": 6}], {"meta2": "data2"})
        tokenlist7.extend(tokenlist8)
        tokenlist9 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}],
                               ["abc", {"meta2": "data2"}])
        self.assertEqual(tokenlist7, tokenlist9)

    def test_tokens(self):
        tokenlist = TokenList([{"id": 1}, {"id": 2}, {"id": 3}])
        self.assertEqual(tokenlist.tokens, [{"id": 1}, {"id": 2}, {"id": 3}])
        tokenlist.tokens = [{"id": 4}, {"id": 5}]
        self.assertEqual(tokenlist.tokens, [{"id": 4}, {"id": 5}])

    def test_to_tree(self):
        tokenlist = TokenList([
            OrderedDict([("id", 2), ("form", "dog"), ("head", 0)]),
            OrderedDict([("id", 1), ("form", "a"), ("head", 2)]),
        ])
        tree = TokenTree(
            token=OrderedDict([("id", 2), ("form", "dog"), ("head", 0)]),
            children=[TokenTree(
                token=OrderedDict([("id", 1), ("form", "a"), ("head", 2)]),
                children=[]
            )]
        )
        self.assertEqual(tokenlist.to_tree(), tree)


class TestSerialize(unittest.TestCase):
    def test_serialize_on_tokenlist(self):
        tokenlist = TokenList([{"id": 1}])
        self.assertEqual(tokenlist.serialize(), serialize(tokenlist))


class TestTokenTree(unittest.TestCase):
    def test_eq(self):
        metadata = {"meta": "data"}

        tokentree1 = TokenTree(token={"id": 1}, children=[TokenTree(token={"id": 2}, children=[])])
        tokentree1.metadata = metadata

        tokentree2 = TokenTree(token={"id": 1}, children=[])
        self.assertNotEqual(tokentree1, tokentree2)

        tokentree2.metadata = metadata
        self.assertNotEqual(tokentree1, tokentree2)

        tokentree2.children = [TokenTree(token={"id": 2}, children=[])]
        self.assertEqual(tokentree1, tokentree2)

    def test_metadata(self):
        tree = TokenTree(token={"id": 1, "form": "hej"}, children=[])
        metadata = {"meta": "data"}
        tree.set_metadata(metadata)
        self.assertEqual(tree.metadata, metadata)


class TestSerializeTree(unittest.TestCase):
    def test_missing_id(self):
        tree = TokenTree(token={"form": "hej"}, children=[])
        with self.assertRaises(ParseException):
            tree.serialize()

    def test_flatten(self):
        tree = TokenTree(
            token=OrderedDict([("id", 2), ("form", "dog")]),
            children=[TokenTree(
                token=OrderedDict([("id", 1), ("form", "a")]),
                children=[]
            )]
        )
        self.assertEqual(
            tree.serialize(),
            dedent("""\
                1\ta
                2\tdog

            """)
        )
        tree = TokenTree(
            token=OrderedDict([("id", 1), ("form", "dog")]),
            children=[TokenTree(
                token=OrderedDict([("id", 2), ("form", "a")]),
                children=[]
            )]
        )
        self.assertEqual(
            tree.serialize(),
            dedent("""\
                1\tdog
                2\ta

            """)
        )


class TestPrintTree(unittest.TestCase):
    def test_print_empty_list(self):
        tree = TokenTree(None, [])
        with self.assertRaises(ParseException):
            capture_print(tree.print_tree)

    def test_tree_without_deprel(self):
        tree = TokenTree(token={"id": 1, "form": "hej"}, children=[])
        with self.assertRaises(ParseException):
            capture_print(tree.print_tree)

    def test_tree_without_id(self):
        tree = TokenTree(token={"form": "hej", "deprel": "nmod"}, children=[])
        with self.assertRaises(ParseException):
            capture_print(tree.print_tree)

    def test_print_simple(self):
        tree = TokenTree(token={"id": "X", "deprel": "Y", "test": "data"}, children=[])
        result = capture_print(tree.print_tree)
        self.assertEqual(result, "(deprel:Y) test:data [X]\n")

    def test_print_with_children(self):
        tree = TokenTree(token={"id": "X", "deprel": "Y", "test": "data"}, children=[
            TokenTree(token={"id": "X", "deprel": "Y", "test": "data"}, children=[]),
            TokenTree(token={"id": "X", "deprel": "Y", "test": "data"}, children=[]),
        ])
        result = capture_print(tree.print_tree)

        self.assertEqual(result, dedent("""\
            (deprel:Y) test:data [X]
                (deprel:Y) test:data [X]
                (deprel:Y) test:data [X]
        """))
