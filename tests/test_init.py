# coding: utf-8
from __future__ import unicode_literals

import io
import unittest
from textwrap import dedent

from conllu import parse, parse_incr
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
        # with self.subTest("parse"):
        self.assertEqual(
            text(parse(data)),
            "[TokenList<The, dog, .>, TokenList<The, dog, .>]"
        )

        # with self.subTest("parse_incr"):
        self.assertEqual(
            text([item for item in parse_incr(io.StringIO(data))]),
            "[TokenList<The, dog, .>, TokenList<The, dog, .>]"
        )

    def test_multi_empty_line_end(self):
        data = dedent("""\
            1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
            2   dog     dog    NOUN   NN   Number=Sing                 5   nmod    _   SpaceAfter=No
            3  .       .      PUNCT  .    _                           5   punct   _   _



            1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
            2   dog     dog    NOUN   NN   Number=Sing                 5   nmod    _   SpaceAfter=No
            3  .       .      PUNCT  .    _                           5   punct   _   _



        """)
        # with self.subTest("parse"):
        self.assertEqual(
            text(parse(data)),
            "[TokenList<The, dog, .>, TokenList<The, dog, .>]"
        )

        # with self.subTest("parse_incr"):
        self.assertEqual(
            text([item for item in parse_incr(io.StringIO(data))]),
            "[TokenList<The, dog, .>, TokenList<The, dog, .>]"
        )
