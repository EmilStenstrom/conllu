# coding: utf-8
from __future__ import unicode_literals

import unittest
from textwrap import dedent

from conllu.compat import capture_print
from conllu.models import TokenList, TokenTree
from conllu.parser import ParseException, serialize


class TestTokenList(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(ParseException):
            TokenList({"id": 1})

class TestSerialize(unittest.TestCase):
    def test_serialize_on_tokenlist(self):
        tokenlist = TokenList([{"id": 1}])
        self.assertEqual(tokenlist.serialize(), serialize(tokenlist))

class TestTokenTree(unittest.TestCase):
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
        tree = TokenTree({"id": 2, "form": "dog"}, [TokenTree({"id": 1, "form": "a"}, [])])
        self.assertEqual(
            tree.serialize(),
            dedent("""\
                1\ta
                2\tdog

            """)
        )
        tree = TokenTree({"id": 1, "form": "dog"}, [TokenTree({"id": 2, "form": "a"}, [])])
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
