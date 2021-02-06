# coding: utf-8
from __future__ import unicode_literals

import unittest
from textwrap import dedent

from conllu.models import Metadata, Token, TokenList, TokenTree
from conllu.parser import ParseException, serialize
from tests.helpers import capture_print


class TestToken(unittest.TestCase):
    def test_xupos_to_xupostag(self):
        token = Token({"id": 1, "xpos": "DT", "upos": "DET"})
        self.assertEqual(token["xpos"], "DT")
        self.assertEqual(token["xpostag"], "DT")
        self.assertEqual(token["upos"], "DET")
        self.assertEqual(token["upostag"], "DET")
        self.assertEqual(token.get("xpos"), "DT")
        self.assertEqual(token.get("xpostag"), "DT")
        self.assertEqual(token.get("upos"), "DET")
        self.assertEqual(token.get("upostag"), "DET")

    def test_xupostag_to_xupos(self):
        token = Token({"id": 1, "xpostag": "DT", "upostag": "DET"})
        self.assertEqual(token["xpos"], "DT")
        self.assertEqual(token["xpostag"], "DT")
        self.assertEqual(token["upos"], "DET")
        self.assertEqual(token["upostag"], "DET")
        self.assertEqual(token.get("xpos"), "DT")
        self.assertEqual(token.get("xpostag"), "DT")
        self.assertEqual(token.get("upos"), "DET")
        self.assertEqual(token.get("upostag"), "DET")

    def test_invalid_key_access(self):
        token = Token({"id": 1, "xpostag": "DT", "upostag": "DET"})
        with self.assertRaises(KeyError):
            token["inexistent_value"]

        self.assertEqual(token.get("inexistent_value"), None)
        self.assertEqual(token.get("inexistent_value", "HEJ"), "HEJ")

    def test_missing_upos_and_upostag(self):
        token = Token({"id": 1})
        self.assertEqual(token["upos"], None)
        self.assertEqual(token.get("upos"), None)


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

    def test_clear(self):
        tokenlist = TokenList([{"id": 1}, {"id": 2}, {"id": 3}], {"meta": "data"})
        tokenlist.clear()
        self.assertEqual(len(tokenlist.tokens), 0)
        self.assertEqual(tokenlist.metadata, Metadata())

    def test_copy(self):
        tokenlist1 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}], {"meta": "data"})
        tokenlist2 = tokenlist1.copy()
        self.assertIsNot(tokenlist1, tokenlist2)
        self.assertEqual(tokenlist1, tokenlist2)

    def test_extend_tokenlist_no_metadata_with_list(self):
        tokenlist1 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}])
        tokenlist2 = [{"id": 4}, {"id": 5}, {"id": 6}]
        tokenlist1.extend(tokenlist2)
        tokenlist3 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}])
        self.assertEqual(tokenlist1, tokenlist3)

    def test_extend_tokenlist_and_merge_metadata(self):
        tokenlist4 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}], {"meta1": "data1"})
        tokenlist5 = TokenList([{"id": 4}, {"id": 5}, {"id": 6}], {"meta2": "data2"})
        tokenlist4.extend(tokenlist5)
        tokenlist6 = TokenList([{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}],
                               {"meta1": "data1", "meta2": "data2"})
        self.assertEqual(tokenlist4, tokenlist6)

    def test_tokens(self):
        tokenlist = TokenList([{"id": 1}, {"id": 2}, {"id": 3}])
        self.assertEqual(tokenlist.tokens, [{"id": 1}, {"id": 2}, {"id": 3}])
        tokenlist.tokens = [{"id": 4}, {"id": 5}]
        self.assertEqual(tokenlist.tokens, [{"id": 4}, {"id": 5}])

    def test_empty(self):
        tokenlist = TokenList()
        self.assertEqual(tokenlist.tokens, [])


class TestParsinigTrickyTrees(unittest.TestCase):
    def assertTreeEqual(self, tree, other):
        self.assertEqual(tree.token, other.token)
        self.assertEqual(len(tree.children), len(other.children))
        for i, child in enumerate(tree.children):
            self.assertTreeEqual(child, other.children[i])

    def test_simple_tree(self):
        tokenlist = TokenList([
            Token([("id", 2), ("form", "dog"), ("head", 0)]),
            Token([("id", 1), ("form", "a"), ("head", 2)]),
        ])
        tree = TokenTree(
            token=Token([("id", 2), ("form", "dog"), ("head", 0)]),
            children=[TokenTree(
                token=Token([("id", 1), ("form", "a"), ("head", 2)]),
                children=[]
            )]
        )
        self.assertTreeEqual(tokenlist.to_tree(), tree)

    def test_removes_negative_nodes(self):
        tokenlist = TokenList([
            Token([("id", 2), ("form", "dog"), ("head", 0)]),
            Token([("id", 1), ("form", "a"), ("head", 2)]),
            Token([("id", 3), ("form", "😍"), ("head", -1)]),
        ])
        tree = TokenTree(
            token=Token([("id", 2), ("form", "dog"), ("head", 0)]),
            children=[TokenTree(
                token=Token([("id", 1), ("form", "a"), ("head", 2)]),
                children=[]
            )]
        )
        self.assertTreeEqual(tokenlist.to_tree(), tree)

    def test_multiple_root_nodes(self):
        tokenlist = TokenList([
            Token([('id', 1), ('form', 'To'), ('head', 0)]),
            Token([('id', 2), ('form', 'appear'), ('head', 1)]),
            Token([('id', 4), ('form', 'EMNLP'), ('head', 0)]),
            Token([('id', 5), ('form', '2014'), ('head', 4)]),
            Token([('id', 6), ('form', 'Yay!'), ('head', 0)]),
        ])
        tree = TokenTree(
            token=Token([("id", 0), ("form", "_"), ("deprel", "root")]),
            children=[
                TokenTree(
                    token=Token([("id", 1), ("form", "To"), ("head", 0)]),
                    children=[TokenTree(
                        token=Token([("id", 2), ("form", "appear"), ("head", 1)]),
                        children=[]
                    )]
                ),
                TokenTree(
                    token=Token([("id", 4), ("form", "EMNLP"), ("head", 0)]),
                    children=[TokenTree(
                        token=Token([("id", 5), ("form", "2014"), ("head", 4)]),
                        children=[]
                    )]
                ),
                TokenTree(
                    token=Token([("id", 6), ("form", "Yay!"), ("head", 0)]),
                    children=[]
                ),
            ]
        )
        self.assertTreeEqual(tokenlist.to_tree(), tree)

    def test_no_root_nodes(self):
        tokenlist = TokenList([
            Token([('id', 1), ('form', 'To'), ('head', 1)]),
            Token([('id', 2), ('form', 'appear'), ('head', 2)]),
        ])
        with self.assertRaises(ParseException):
            tokenlist.to_tree()


class TestSerialize(unittest.TestCase):
    def test_serialize_on_tokenlist(self):
        tokenlist = TokenList([{"id": 1}])
        self.assertEqual(tokenlist.serialize(), serialize(tokenlist))


class TestFilter(unittest.TestCase):
    def test_basic_filtering(self):
        tokenlist = TokenList([
            {"id": 1, "form": "a", "field": "x"},
            {"id": 2, "form": "dog", "field": "x"},
        ])
        self.assertEqual(
            tokenlist.filter(id=0),
            TokenList([])
        )
        self.assertEqual(
            tokenlist.filter(id=1),
            TokenList([{"id": 1, "form": "a", "field": "x"}])
        )
        self.assertEqual(
            tokenlist.filter(),
            tokenlist
        )
        self.assertEqual(
            tokenlist.filter(field="x"),
            tokenlist
        )

    def test_and_filtering(self):
        tokenlist = TokenList([
            {"id": 1, "form": "a", "field": "x"},
            {"id": 2, "form": "dog", "field": "x"},
            {"id": 3, "form": "dog", "field": "y"},
        ])
        self.assertEqual(
            tokenlist.filter(field="x", id=2),
            TokenList([
                {"id": 2, "form": "dog", "field": "x"},
            ])
        )
        self.assertEqual(
            tokenlist.filter(field="x", id=3),
            TokenList([])
        )

    def test_deep_filtering(self):
        tokenlist = TokenList([
            {"form": "The", "feats": Token([('Definite', 'Def'), ('PronType', 'Art')])},
            {"form": "quick", "feats": Token([('Degree', 'Pos')])},
            {"form": "brown", "feats": Token([('Degree', 'Pos')])},
            {"form": "fox", "feats": Token([('Number', 'Sing')])},
        ])
        self.assertEqual(
            tokenlist.filter(feats__Degree="Pos"),
            TokenList([
                {"form": "quick", "feats": Token([('Degree', 'Pos')])},
                {"form": "brown", "feats": Token([('Degree', 'Pos')])},
            ])
        )
        self.assertEqual(
            tokenlist.filter(form="brown", feats__Degree="Pos"),
            TokenList([
                {"form": "brown", "feats": Token([('Degree', 'Pos')])},
            ])
        )
        self.assertEqual(
            tokenlist.filter(form="brown", feats__Degree="Pos", id=1),
            TokenList([])
        )
        self.assertEqual(
            tokenlist.filter(unknown__property__value="undefined"),
            TokenList([])
        )
        self.assertEqual(
            tokenlist.filter(unknown___property____value="undefined"),
            TokenList([])
        )

    def test_nested_filtering(self):
        tokenlist = TokenList([
            {"form": "The", "feats": Token([('Definite', 'Def'), ('PronType', 'Art')])},
            {"form": "quick", "feats": Token([('Degree', 'Pos')])},
            {"form": "brown", "feats": Token([('Degree', 'Pos')])},
            {"form": "fox", "feats": Token([('Number', 'Sing')])},
        ])
        self.assertEqual(
            tokenlist.filter(feats__Degree="Pos").filter(form="brown"),
            TokenList([
                {"form": "brown", "feats": Token([('Degree', 'Pos')])},
            ])
        )
        self.assertEqual(
            tokenlist.filter(form="brown").filter(feats__Degree="Pos"),
            TokenList([
                {"form": "brown", "feats": Token([('Degree', 'Pos')])},
            ])
        )
        self.assertEqual(
            tokenlist.filter(form="brown").filter(feats__Degree="Pos").filter(),
            TokenList([
                {"form": "brown", "feats": Token([('Degree', 'Pos')])},
            ])
        )
        self.assertEqual(
            tokenlist.filter(form="brown").filter(feats__Degree="Pos").filter(id=0),
            TokenList([])
        )

    def test_lambda_basic_filtering(self):
        tokenlist = TokenList([
            Token({'id': (1, '-', 2), 'form': "It's", 'lemma': '_', 'feats': None}),
            Token({'id': 1, 'form': 'It', 'lemma': 'it'}),
            Token({'id': 2, 'form': "'s", 'lemma': 'be'})
        ])

        self.assertEqual(
            tokenlist.filter(id=lambda x: type(x) is int),
            TokenList([
                Token({'id': 1, 'form': 'It', 'lemma': 'it'}),
                Token({'id': 2, 'form': "'s", 'lemma': 'be'})
            ])
        )
        self.assertEqual(
            tokenlist.filter(lemma=lambda x: x.startswith('b')),
            TokenList([
                Token({'id': 2, 'form': "'s", 'lemma': 'be'})
            ])
        )

    def test_lambda_deep_filtering(self):
        tokenlist = TokenList([
            Token({'id': (1, '-', 2), 'feats': None}),
            Token({'id': 1, 'feats': {'Case': 'Nom', 'Number': 'Sing'}}),
            Token({'id': 2, 'feats': {'Mood': 'Ind', 'Number': 'Sing'}})
        ])

        self.assertEqual(
            tokenlist.filter(feats__Mood=lambda x: x == 'Ind'),
            TokenList([
                Token({'id': 2, 'feats': {'Mood': 'Ind', 'Number': 'Sing'}})
            ])
        )

        self.assertEqual(
            tokenlist.filter(feats__Number=lambda x: x == 'Sing'),
            TokenList([
                Token({'id': 1, 'feats': {'Case': 'Nom', 'Number': 'Sing'}}),
                Token({'id': 2, 'feats': {'Mood': 'Ind', 'Number': 'Sing'}})
            ])
        )


class TestTokenTree(unittest.TestCase):
    def test_eq(self):
        metadata = {"meta": "data"}

        tokentree1 = TokenTree(token={"id": 1}, children=[TokenTree(token={"id": 2}, children=[])])
        tokentree1.metadata = metadata

        tokentree2 = TokenTree(token={"id": 1}, children=[])
        self.assertNotEqual(tokentree1, tokentree2)

        # Not equal with a plain dict
        self.assertNotEqual(tokentree2, {"id": 1})

        tokentree2.metadata = metadata
        self.assertNotEqual(tokentree1, tokentree2)

        tokentree2.children = [TokenTree(token={"id": 2}, children=[])]
        self.assertEqual(tokentree1, tokentree2)

    def test_metadata(self):
        tree = TokenTree(token={"id": 1, "form": "hej"}, children=[])
        metadata = {"meta": "data"}
        tree.set_metadata(metadata)
        self.assertEqual(tree.metadata, metadata)

        tree = TokenTree(token={"id": 1, "form": "hej"}, children=[], metadata={"meta": "data"})
        self.assertEqual(tree.metadata, metadata)


class TestSerializeTree(unittest.TestCase):
    def test_missing_id(self):
        tree = TokenTree(token={"form": "hej"}, children=[])
        with self.assertRaises(ParseException):
            tree.serialize()

    def test_flatten(self):
        tree = TokenTree(
            token=Token([("id", 2), ("form", "dog")]),
            children=[TokenTree(
                token=Token([("id", 1), ("form", "a")]),
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
            token=Token([("id", 1), ("form", "dog")]),
            children=[TokenTree(
                token=Token([("id", 2), ("form", "a")]),
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
