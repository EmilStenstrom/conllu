# coding: utf-8
from __future__ import unicode_literals

import re
import unittest
from collections import OrderedDict
from io import StringIO
from textwrap import dedent

from conllu import parse, parse_incr, parse_tree, parse_tree_incr
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


data2 = dedent("""\
    1	In	in	in	IN	IN	_	_	43	20	LOC	ADV	_	_	_	_	_	_	_	_	AM-LOC
    2	an	an	an	DT	DT	_	_	5	5	NMOD	NMOD	_	_	_	_	_	_	_	_	_
    3	Oct.	oct.	oct.	NNP	NNP	_	_	4	4	NMOD	NMOD	_	_	_	_	_	_	_	_	_
    4	19	19	19	CD	CD	_	_	5	5	NMOD	NMOD	_	_	AM-TMP	_	_	_	_	_	_
    5	review	review	review	NN	NN	_	_	1	1	PMOD	PMOD	Y	review.01	_	_	_	_	_	_	_
    6	of	of	of	IN	IN	_	_	5	5	NMOD	NMOD	_	_	A1	_	_	_	_	_	_
    7	``	``	``	``	``	_	_	9	6	P	P	_	_	_	_	_	_	_	_	_
    8	The	the	the	DT	DT	_	_	9	9	NMOD	NMOD	_	_	_	_	_	_	_	_	_
    9	Misanthrope	misanthrope	misanthrope	NN	NN	_	_	6	6	PMOD	PMOD	_	_	_	_	_	_	_	_	_
    10	''	''	''	''	''	_	_	9	5	P	P	_	_	_	_	_	_	_	_	_
    11	at	at	at	IN	IN	_	_	9	5	LOC	LOC	_	_	_	_	_	_	_	_	_
    12	Chicago	chicago	chicago	NNP	NNP	_	_	15	15	NMOD	NMOD	_	_	_	_	_	_	_	_	_
    13	's	's	's	POS	POS	_	_	12	12	SUFFIX	SUFFIX	_	_	_	_	_	_	_	_	_
    14	Goodman	goodman	goodman	NNP	NNP	_	_	15	15	NAME	NAME	_	_	_	_	_	_	_	_	_
    15	Theatre	theatre	theatre	NNP	NNP	_	_	11	11	PMOD	PMOD	_	_	_	_	_	_	_	_	_
    16	(	-lrb-	-lrb-	(	(	_	_	20	20	P	P	_	_	_	_	_	_	_	_	_
    17	``	``	``	``	``	_	_	20	19	P	P	_	_	_	_	_	_	_	_	_
    18	Revitalized	revitalize	revitalize	VBN	VBN	_	_	19	19	NMOD	NMOD	Y	revitalize.01	_	_	_	_	_	_	_
    19	Classics	classics	classics	NNS	NNS	_	_	20	20	SBJ	SBJ	_	_	_	A1	A0	A1	_	_	_
    20	Take	take	take	VBP	VB	_	_	5	43	PRN	OBJ	Y	take.01	_	_	_	_	_	_	_
    21	the	the	the	DT	DT	_	_	22	22	NMOD	NMOD	_	_	_	_	_	_	_	_	_
    22	Stage	stage	stage	NN	NNP	_	_	20	20	OBJ	OBJ	Y	stage.02	_	_	A1	_	_	_	_
    23	in	in	in	IN	IN	_	_	20	22	LOC	LOC	_	_	_	_	AM-LOC	_	_	_	_
    24	Windy	windy	windy	NNP	NNP	_	_	25	25	NAME	NAME	_	_	_	_	_	_	_	_	_
    25	City	city	city	NNP	NNP	_	_	23	23	PMOD	PMOD	_	_	_	_	_	_	_	_	_
    26	,	,	,	,	,	_	_	20	43	P	P	_	_	_	_	_	_	_	_	_
    27	''	''	''	''	''	_	_	20	43	P	P	_	_	_	_	_	_	_	_	_   
    28	Leisure	leisure	leisure	NNP	NNP	_	_	30	30	NAME	NAME	_	_	_	_	_	_	_	_	_
    29	&	&	&	CC	CC	_	_	30	30	NAME	NAME	_	_	_	_	_	_	_	_	_
    30	Arts	arts	arts	NNS	NNS	_	_	20	34	TMP	NMOD	_	_	_	_	_	_	_	_	_
    31	)	-rrb-	-rrb-	)	)	_	_	20	30	P	P	_	_	_	_	_	_	_	_	_
    32	,	,	,	,	,	_	_	43	34	P	P	_	_	_	_	_	_	_	_	_
    33	the	the	the	DT	DT	_	_	34	34	NMOD	NMOD	_	_	_	_	_	_	_	_	_
    34	role	role	role	NN	NN	_	_	43	43	SBJ	SBJ	Y	role.01	_	_	_	_	_	A1	A1
    35	of	of	of	IN	IN	_	_	34	34	NMOD	NMOD	_	_	_	_	_	_	A1	_	_
    36	Celimene	celimene	celimene	NNP	NNP	_	_	35	35	PMOD	PMOD	_	_	_	_	_	_	_	_	_
    37	,	,	,	,	,	_	_	34	34	P	P	_	_	_	_	_	_	_	_	_
    38	played	play	play	VBN	VBN	_	_	34	34	APPO	APPO	Y	play.02	_	_	_	_	_	_	_
    39	by	by	by	IN	IN	_	_	38	38	LGS	LGS	_	_	_	_	_	_	_	A0	_
    40	Kim	kim	kim	NNP	NNP	_	_	41	41	NAME	NAME	_	_	_	_	_	_	_	_	_
    41	Cattrall	cattrall	cattrall	NNP	NNP	_	_	39	39	PMOD	PMOD	_	_	_	_	_	_	A0	_	_
    42	,	,	,	,	,	_	_	34	34	P	P	_	_	_	_	_	_	_	_	_
    43	was	be	be	VBD	VBD	_	_	0	0	ROOT	ROOT	_	_	_	_	_	_	_	_	_
    44	mistakenly	mistakenly	mistakenly	RB	RB	_	_	45	45	MNR	AMOD	_	_	_	_	_	_	_	_	AM-MNR
    45	attributed	attribute	attribute	VBN	VBN	_	_	43	43	VC	PRD	Y	attribute.01	_	_	_	_	_	_	_
    46	to	to	to	TO	TO	_	_	45	45	ADV	AMOD	_	_	_	_	_	_	_	_	A2
    47	Christina	christina	christina	NNP	NNP	_	_	48	48	NAME	NAME	_	_	_	_	_	_	_	_	_
    48	Haag	haag	haag	NNP	NNP	_	_	46	46	PMOD	PMOD	_	_	_	_	_	_	_	_	_
    49	.	.	.	.	.	_	_	43	43	P	P	_	_	_	_	_	_	_	_	_

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

    def test_parse_incr(self):
        self.assertEqual(parse(data), list(parse_incr(StringIO(data))))

    def test_parse_tree_incr(self):
        self.assertEqual(parse_tree(data), list(parse_tree_incr(StringIO(data))))

    def test_parse_CoNLL2009(self):
        sentences = parse(data2, CoNLL2009=True)
        self.assertEqual(len(sentences), 1)
        self.assertEqual({45:"AM-LOC"}, sentences[0][0]['apreds'])
        self.assertEqual({5:"AM-TMP"}, sentences[0][3]['apreds'])
        self.assertEqual({5:"A1"}, sentences[0][5]['apreds'])
        self.assertEqual({}, sentences[0][14]['apreds'])
        self.assertEqual({18:"A1", 20:"A0", 22:"A1"}, sentences[0][18]['apreds'])
        self.assertEqual({45:"A2"}, sentences[0][45]['apreds'])
        self.assertEqual({}, sentences[0][48]['apreds'])


@testlabel("integration")
class TestTrickyCases(unittest.TestCase):
    maxDiff = None

    def test_fixtures(self):
        from tests.fixtures import TESTCASES

        for testcase in TESTCASES:
            self.assertEqual(parse(testcase)[0].serialize(), testcase)
