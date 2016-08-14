from collections import OrderedDict
import unittest
from conllu.parser import parse

data = """
1\tThe\tthe\tDET\tDT\tDefinite=Def|PronType=Art\t4\tdet\t_\t_
2\tquick\tquick\tADJ\tJJ\tDegree=Pos\t4\tamod\t_\t_
3\tbrown\tbrown\tADJ\tJJ\tDegree=Pos\t4\tamod\t_\t_
4\tfox\tfox\tNOUN\tNN\tNumber=Sing\t5\tnsubj\t_\t_
5\tjumps\tjump\tVERB\tVBZ\tMood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin\t0\troot\t_\t_
6\tover\tover\tADP\tIN\t_\t9\tcase\t_\t_
7\tthe\tthe\tDET\tDT\tDefinite=Def|PronType=Art\t9\tdet\t_\t_
8\tlazy\tlazy\tADJ\tJJ\tDegree=Pos\t9\tamod\t_\t_
9\tdog\tdog\tNOUN\tNN\tNumber=Sing\t5\tnmod\t_\tSpaceAfter=No
10\t.\t.\tPUNCT\t.\t_\t5\tpunct\t_\t_

"""

expected = [[
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
    ]),
    OrderedDict([
        ('id', 2),
        ('form', 'quick'),
        ('lemma', 'quick'),
        ('upostag', 'ADJ'),
        ('xpostag', 'JJ'),
        ('feats', OrderedDict([('Degree', 'Pos')])),
        ('head', 4),
        ('deprel', 'amod'),
        ('deps', None),
        ('misc', None)
    ]),
    OrderedDict([
        ('id', 3),
        ('form', 'brown'),
        ('lemma', 'brown'),
        ('upostag', 'ADJ'),
        ('xpostag', 'JJ'),
        ('feats', OrderedDict([('Degree', 'Pos')])),
        ('head', 4),
        ('deprel', 'amod'),
        ('deps', None),
        ('misc', None)
    ]),
    OrderedDict([
        ('id', 4),
        ('form', 'fox'),
        ('lemma', 'fox'),
        ('upostag', 'NOUN'),
        ('xpostag', 'NN'),
        ('feats', OrderedDict([('Number', 'Sing')])),
        ('head', 5),
        ('deprel', 'nsubj'),
        ('deps', None),
        ('misc', None)
    ]),
    OrderedDict([
        ('id', 5),
        ('form', 'jumps'),
        ('lemma', 'jump'),
        ('upostag', 'VERB'),
        ('xpostag', 'VBZ'),
        ('feats', OrderedDict([
            ('Mood', 'Ind'),
            ('Number', 'Sing'),
            ('Person', '3'),
            ('Tense', 'Pres'),
            ('VerbForm', 'Fin')
        ])),
        ('head', 0),
        ('deprel', 'root'),
        ('deps', None),
        ('misc', None)
    ]),
    OrderedDict([
        ('id', 6),
        ('form', 'over'),
        ('lemma', 'over'),
        ('upostag', 'ADP'),
        ('xpostag', 'IN'),
        ('feats', None),
        ('head', 9),
        ('deprel', 'case'),
        ('deps', None),
        ('misc', None)
    ]),
    OrderedDict([
        ('id', 7),
        ('form', 'the'),
        ('lemma', 'the'),
        ('upostag', 'DET'),
        ('xpostag', 'DT'),
        ('feats', OrderedDict([('Definite', 'Def'), ('PronType', 'Art')])),
        ('head', 9),
        ('deprel', 'det'),
        ('deps', None),
        ('misc', None)
    ]),
    OrderedDict([
        ('id', 8),
        ('form', 'lazy'),
        ('lemma', 'lazy'),
        ('upostag', 'ADJ'),
        ('xpostag', 'JJ'),
        ('feats', OrderedDict([('Degree', 'Pos')])),
        ('head', 9),
        ('deprel', 'amod'),
        ('deps', None),
        ('misc', None)
    ]),
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
        ('misc', OrderedDict([('SpaceAfter', 'No')]))
    ]),
    OrderedDict([
        ('id', 10),
        ('form', '.'),
        ('lemma', '.'),
        ('upostag', 'PUNCT'),
        ('xpostag', '.'),
        ('feats', None),
        ('head', 5),
        ('deprel', 'punct'),
        ('deps', None),
        ('misc', None)
    ])
]]

class TestIntegration(unittest.TestCase):
    def test_parsing(self):
        self.assertEqual(parse(data), expected)
