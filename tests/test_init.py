# coding: utf-8
from __future__ import unicode_literals

import unittest
from textwrap import dedent

from conllu import parse, parse_tree
from conllu.compat import text


class TestParse(unittest.TestCase):
    def test_multiple_sentences(self):
        data = dedent("""\
            1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
            2   dog     dog    NOUN   NN   Number=Sing                 5   nmod    _   SpaceAfter=No
            3  .       .      PUNCT  .    _                           5   punct   _   _

            1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
            2   dog     dog    NOUN   NN   Number=Sing                 5   nmod    _   SpaceAfter=No
            3  .       .      PUNCT  .    _                           5   punct   _   _

        """)
        self.assertEqual(
            text(parse(data)),
            "[TokenList<The, dog, .>, TokenList<The, dog, .>]"
        )
