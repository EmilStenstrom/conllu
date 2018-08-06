# coding: utf-8
from __future__ import unicode_literals

import re
import unittest
from collections import OrderedDict
from textwrap import dedent

from conllu import parse, parse_tree
from conllu.compat import capture_print, text
from tests.helpers import testlabel

data = dedent("""\
    # text = The quick brown fox jumps over the lazy dog.
    1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
    2   quick   quick  ADJ    JJ   Degree=Pos                  4   amod    _   _
    3   brown   brown  ADJ    JJ   Degree=Pos                  4   amod    _   _
    4   fox     fox    NOUN   NN   Number=Sing                 5   nsubj   _   _
    5   jumps   jump   VERB   VBZ  Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin   0   root    _   _
    6   over    over   ADP    IN   _                           9   case    _   _
    7   the     the    DET    DT   Definite=Def|PronType=Art   9   det     _   _
    8   lazy    lazy   ADJ    JJ   Degree=Pos                  9   amod    _   _
    9   dog     dog    NOUN   NN   Number=Sing                 5   nmod    _   SpaceAfter=No
    10  .       .      PUNCT  .    _                           5   punct   _   _

""")
data = re.sub(r"  +", r"\t", data)

@testlabel("integration")
class TestParse(unittest.TestCase):
    maxDiff = None

    def test_parse(self):
        sentences = parse(data)
        self.assertEqual(len(sentences), 1)

        sentence = sentences[0]

        self.assertEqual(text(sentence), "TokenList<The, quick, brown, fox, jumps, over, the, lazy, dog, .>")

        self.assertEqual(
            sentence[0],
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
        self.assertEqual(
            sentence[8],
            OrderedDict([
                ('id', 9),
                ('form', 'dog'),
                ('lemma', 'dog'),
                ('upostag', 'NOUN'),
                ('xpostag', 'NN'),
                ('feats', OrderedDict([('Number', 'Sing')])),
                ('head', 5),
                ('deprel', 'nmod'),
                ('deps', None),
                ('misc', OrderedDict([("SpaceAfter", "No")]))
            ])
        )
        self.assertEqual(
            [token["form"] for token in sentence],
            "The quick brown fox jumps over the lazy dog .".split(" ")
        )

        self.assertEqual(
            sentence.metadata["text"],
            "The quick brown fox jumps over the lazy dog."
        )

    def test_parse_tree(self):
        sentences = parse_tree(data)
        self.assertEqual(len(sentences), 1)

        root = sentences[0]
        self.assertEqual(text(root), "TokenTree<token={id=5, form=jumps}, children=[...]>")

        self.assertEqual(
            root.token,
            OrderedDict([
                ('id', 5),
                ('form', 'jumps'),
                ('lemma', 'jump'),
                ('upostag', 'VERB'),
                ('xpostag', 'VBZ'),
                ('feats', OrderedDict([
                    ("Mood", "Ind"),
                    ("Number", "Sing"),
                    ("Person", "3"),
                    ("Tense", "Pres"),
                    ("VerbForm", "Fin"),
                ])),
                ('head', 0),
                ('deprel', 'root'),
                ('deps', None),
                ('misc', None)
            ])
        )

        self.assertEqual(
            [text(child) for child in root.children],
            [
                "TokenTree<token={id=4, form=fox}, children=[...]>",
                "TokenTree<token={id=9, form=dog}, children=[...]>",
                "TokenTree<token={id=10, form=.}, children=None>",
            ]
        )

        self.assertEqual(
            root.metadata["text"],
            "The quick brown fox jumps over the lazy dog."
        )

        self.assertEqual(root.serialize(), data)

        self.assertEqual(
            capture_print(root.print_tree),
            dedent("""\
                (deprel:root) form:jumps lemma:jump upostag:VERB [5]
                    (deprel:nsubj) form:fox lemma:fox upostag:NOUN [4]
                        (deprel:det) form:The lemma:the upostag:DET [1]
                        (deprel:amod) form:quick lemma:quick upostag:ADJ [2]
                        (deprel:amod) form:brown lemma:brown upostag:ADJ [3]
                    (deprel:nmod) form:dog lemma:dog upostag:NOUN [9]
                        (deprel:case) form:over lemma:over upostag:ADP [6]
                        (deprel:det) form:the lemma:the upostag:DET [7]
                        (deprel:amod) form:lazy lemma:lazy upostag:ADJ [8]
                    (deprel:punct) form:. lemma:. upostag:PUNCT [10]
            """)
        )

@testlabel("integration")
class TestTrickyCases(unittest.TestCase):
    maxDiff = None

    def test_fixtures(self):
        from tests.fixtures import TESTCASES

        for testcase in TESTCASES:
            self.assertEqual(parse(testcase)[0].serialize(), testcase)
