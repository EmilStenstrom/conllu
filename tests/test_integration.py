import re
import unittest
from io import StringIO
from textwrap import dedent

import pytest

from conllu import parse, parse_incr, parse_tree, parse_tree_incr
from conllu.models import Token, TokenList
from conllu.parser import parse_dict_value, parse_int_value
from tests.helpers import capture_print


@pytest.mark.integration
class TestParse(unittest.TestCase):
    maxDiff = None

    data = re.sub(r"  +", r"\t", dedent("""\
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

    """))

    def test_parse(self):
        sentences = parse(self.data)
        self.assertEqual(len(sentences), 1)

        sentence = sentences[0]

        self.assertEqual(
            str(sentence),
            "TokenList<The, quick, brown, fox, jumps, over, the, lazy, dog, ."
            ", metadata={text: \"The quick brown fox jumps over the lazy dog.\"}>"
        )

        self.assertEqual(
            sentence[0],
            Token([
                ('id', 1),
                ('form', 'The'),
                ('lemma', 'the'),
                ('upos', 'DET'),
                ('xpos', 'DT'),
                ('feats', Token([('Definite', 'Def'), ('PronType', 'Art')])),
                ('head', 4),
                ('deprel', 'det'),
                ('deps', None),
                ('misc', None)
            ])
        )
        self.assertEqual(
            sentence[8],
            Token([
                ('id', 9),
                ('form', 'dog'),
                ('lemma', 'dog'),
                ('upos', 'NOUN'),
                ('xpos', 'NN'),
                ('feats', Token([('Number', 'Sing')])),
                ('head', 5),
                ('deprel', 'nmod'),
                ('deps', None),
                ('misc', Token([("SpaceAfter", "No")]))
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
        sentences = parse_tree(self.data)
        self.assertEqual(len(sentences), 1)

        root = sentences[0]
        self.assertEqual(str(root), "TokenTree<token={id=5, form=jumps}, children=[...]>")

        self.assertEqual(
            root.token,
            Token([
                ('id', 5),
                ('form', 'jumps'),
                ('lemma', 'jump'),
                ('upos', 'VERB'),
                ('xpos', 'VBZ'),
                ('feats', Token([
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
            [str(child) for child in root.children],
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

        self.assertEqual(root.serialize(), self.data)

        self.assertEqual(
            capture_print(root.print_tree),
            dedent("""\
                (deprel:root) form:jumps lemma:jump upos:VERB [5]
                    (deprel:nsubj) form:fox lemma:fox upos:NOUN [4]
                        (deprel:det) form:The lemma:the upos:DET [1]
                        (deprel:amod) form:quick lemma:quick upos:ADJ [2]
                        (deprel:amod) form:brown lemma:brown upos:ADJ [3]
                    (deprel:nmod) form:dog lemma:dog upos:NOUN [9]
                        (deprel:case) form:over lemma:over upos:ADP [6]
                        (deprel:det) form:the lemma:the upos:DET [7]
                        (deprel:amod) form:lazy lemma:lazy upos:ADJ [8]
                    (deprel:punct) form:. lemma:. upos:PUNCT [10]
            """)
        )

    def test_parse_incr(self):
        self.assertEqual(parse(self.data), list(parse_incr(StringIO(self.data))))

    def test_parse_incr_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            list(parse_incr("SOME STRING DATA"))

    def test_parse_tree_incr(self):
        self.assertEqual(parse_tree(self.data), list(parse_tree_incr(StringIO(self.data))))


@pytest.mark.integration
class TestTrickyCases(unittest.TestCase):
    maxDiff = None

    def test_parse_and_serialize(self):
        from tests.fixtures import TESTCASES

        for testcase in TESTCASES:
            self.assertEqual(parse(testcase)[0].serialize(), testcase)

    def test_parse_tree_and_serialize(self):
        from tests.fixtures import TESTCASES

        for testcase in TESTCASES:
            data = parse(testcase)
            testcase_without_range_and_elided = TokenList([
                token
                for token in data[0]
                if isinstance(token["id"], int)
            ], metadata=data[0].metadata)
            self.assertEqual(parse_tree(testcase)[0].serialize(), testcase_without_range_and_elided.serialize())


@pytest.mark.integration
class TestParseCoNLLUPlus(unittest.TestCase):
    def test_parse_conllu_plus(self):
        # Note: global.columns affects both sentences
        data = dedent("""\
            # global.columns = ID FORM UPOS HEAD DEPREL MISC PARSEME:MWE
            # source_sent_id = conllu http://hdl.handle.net/11234/1-2837 UD_German-GSD/de_gsd-ud-train.conllu
            # sent_id = train-s16
            # text = Der CDU-Politiker strebt
            1\tDer\tDET\t2\tdet\t_\t*
            2\tCDU\tPROPN\t4\tcompound\tSpaceAfter=No\t*
            3\t-\tPUNCT\t2\tpunct\tSpaceAfter=No\t*
            4\tPolitiker\tNOUN\t5\tnsubj\t_\t*
            5\tstrebt\tVERB\t0\troot\t_\t2:VPC.full

            # source_sent_id = conllu http://hdl.handle.net/11234/1-2837 UD_German-GSD/de_gsd-ud-train.conllu
            # sent_id = train-s17
            # text = Der ortsüblichen Vergleichsmiete orientieren.
            1\tDer\tDET\t19\tdet\t_\t*
            2\tortsüblichen\tADJ\t19\tamod\t_\t*
            3\tVergleichsmiete\tNOUN\t20\tobl\t_\t*
            4\torientieren\tVERB\t8\tacl\tSpaceAfter=No\t1
            5\t.\tPUNCT\t5\tpunct\t_\t*
        """)

        sentences = parse(data)

        self.assertEqual(
            [
                {"form": token["form"], "parseme:mwe": token["parseme:mwe"]}
                for token in sentences[0]
            ],
            [
                {"form": "Der", "parseme:mwe": "*"},
                {"form": "CDU", "parseme:mwe": "*"},
                {"form": "-", "parseme:mwe": "*"},
                {"form": "Politiker", "parseme:mwe": "*"},
                {"form": "strebt", "parseme:mwe": "2:VPC.full"},
            ]
        )
        self.assertEqual(sentences[0].metadata, {
            "global.columns": "ID FORM UPOS HEAD DEPREL MISC PARSEME:MWE",
            "source_sent_id": "conllu http://hdl.handle.net/11234/1-2837 UD_German-GSD/de_gsd-ud-train.conllu",
            "sent_id": "train-s16",
            "text": "Der CDU-Politiker strebt",
        })
        self.assertEqual(
            [
                {"form": token["form"], "parseme:mwe": token["parseme:mwe"]}
                for token in sentences[1]
            ],
            [
                {"form": "Der", "parseme:mwe": "*"},
                {"form": "ortsüblichen", "parseme:mwe": "*"},
                {"form": "Vergleichsmiete", "parseme:mwe": "*"},
                {"form": "orientieren", "parseme:mwe": "1"},
                {"form": ".", "parseme:mwe": "*"},
            ]
        )
        self.assertEqual(sentences[1].metadata, {
            "source_sent_id": "conllu http://hdl.handle.net/11234/1-2837 UD_German-GSD/de_gsd-ud-train.conllu",
            "sent_id": "train-s17",
            "text": "Der ortsüblichen Vergleichsmiete orientieren.",
        })


@pytest.mark.integration
class TestParseCoNLL2009(unittest.TestCase):
    def test_parse_CoNLL2009_1(self):
        data = dedent("""\
            #\tid\tform\tlemma\tplemma\tpos\tppos\tfeats\tpfeats\thead\tphead\tdeprel\tpdeprel\tfillpred\tpred\tapreds
            1\tZ\tz\tz\tR\tR\tSubPOS=R|Cas=2\tSubPOS=R|Cas=2\t10\t10\tAuxP\tAuxP\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_
            2\ttéto\ttento\ttento\tP\tP\tSubPOS=D|Gen=F|Num=S|Cas=2\tSubPOS=D|Gen=F|Num=S|Cas=2\t3\t3\tAtr\tAtr\tY\ttento\t_\tRSTR\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_
            3\tknihy\tkniha\tkniha\tN\tN\tSubPOS=N|Gen=F|Num=S|Cas=2|Neg=A\tSubPOS=N|Gen=F|Num=S|Cas=2|Neg=A\t1\t1\tAdv\tAdv\tY\tkniha\t_\t_\t_\t_\t_\t_\t_\tDIR1\t_\t_\t_\t_\t_\t_\t_\t_

        """)

        sentences = parse(
            data,
            fields=(
                'id', 'form', 'lemma', 'plemma', 'pos', 'ppos', 'feats', 'pfeats',
                'head', 'phead', 'deprel', 'pdeprel', 'fillpred', 'pred', 'apreds'
            ),
            field_parsers={
                "pfeats": lambda line, i: parse_dict_value(line[i]),
                "phead": lambda line, i: parse_int_value(line[i]),
                "apreds": lambda line, i: [
                    apred_field if apred_field != "_" else None
                    for apred_field in line[i:len(line)]
                ],
            },
        )
        self.assertEqual(
            sentences[0][2],
            Token([
                ('id', 3),
                ('form', 'knihy'),
                ('lemma', 'kniha'),
                ('plemma', 'kniha'),
                ('pos', 'N'),
                ('ppos', 'N'),
                ('feats', Token([
                    ('SubPOS', 'N'),
                    ('Gen', 'F'),
                    ('Num', 'S'),
                    ('Cas', '2'),
                    ('Neg', 'A')
                ])),
                ('pfeats', Token([
                    ('SubPOS', 'N'),
                    ('Gen', 'F'),
                    ('Num', 'S'),
                    ('Cas', '2'),
                    ('Neg', 'A')
                ])),
                ('head', 1),
                ('phead', 1),
                ('deprel', 'Adv'),
                ('pdeprel', 'Adv'),
                ('fillpred', 'Y'),
                ('pred', 'kniha'),
                ('apreds', [
                    None, None, None, None, None, None, None, 'DIR1',
                    None, None, None, None, None, None, None, None
                ])
            ])
        )

    def test_parse_CoNLL2009_2(self):
        data = dedent("""\
            #\tid='1'-document_id='36:1047'-span='1'
            1\t+\t+\tPunc\tPunc\t_\t0\tROOT\t_\t_
            2\tIn\tin\tr\tr\tr|-|-|-|-|-|-|-|-\t5\tAuxP\t_\t_
            3\tDei\tDeus\tn\tPropn\tn|-|s|-|-|-|m|g|-\t4\tATR\t_\t_
            4\tnomine\tnomen\tn\tn\tn|-|s|-|-|-|n|b|-\t2\tADV\t_\t_
            5\tregnante\tregno\tt\tt\tt|-|s|p|p|a|m|b|-\t0\tADV\t_\t_

        """)

        sentences = parse(
            data,
            fields=(
                'id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc'
            ),
            field_parsers={
                "feats": lambda line, i: [feat for feat in line[i].split("|")]
            }
        )
        self.assertEqual(
            sentences[0][4],
            Token([
                ('id', 5),
                ('form', 'regnante'),
                ('lemma', 'regno'),
                ('upostag', 't'),
                ('xpostag', 't'),
                ('feats', ['t', '-', 's', 'p', 'p', 'a', 'm', 'b', '-']),
                ('head', 0),
                ('deprel', 'ADV'),
                ('deps', None),
                ('misc', None),
            ])
        )
        self.assertEqual(
            sentences[0].metadata,
            Token([
                ('id', "'1'-document_id='36:1047'-span='1'")
            ])
        )
