# coding: utf-8
from __future__ import unicode_literals

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
