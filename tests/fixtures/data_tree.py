# encoding: utf-8
from __future__ import unicode_literals
from collections import OrderedDict
from conllu.tree_helpers import TreeNode

data1_tree = [
    TreeNode(
        data=OrderedDict([
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
            ('misc', None)]),
        children=[
            TreeNode(
                data=OrderedDict([
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
                children=[
                    TreeNode(
                        data=OrderedDict([
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
                        children=[]
                    ),
                    TreeNode(
                        data=OrderedDict([
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
                        children=[]
                    ),
                    TreeNode(
                        data=OrderedDict([
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
                        children=[]
                    )
                ]
            ),
            TreeNode(
                data=OrderedDict([
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
                children=[
                    TreeNode(
                        data=OrderedDict([
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
                        children=[]
                    ),
                    TreeNode(
                        data=OrderedDict([
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
                        children=[]
                    ),
                    TreeNode(
                        data=OrderedDict([
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
                        children=[]
                    )
                ]
            ),
            TreeNode(
                data=OrderedDict([
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
                ]),
                children=[]
            )
        ]
    )
]

data5_tree = [
    TreeNode(
        data=OrderedDict([
            ('id', 2),
            ('form', 'längtar'),
            ('lemma', 'längta'),
            ('upostag', 'VERB'),
            ('xpostag', 'VBP'),
            ('feats', OrderedDict([
                ('Mood', 'Ind'),
                ('Tense', 'Pres'),
                ('VerbForm', 'Fin'),
                ('Voice', 'Act')
            ])),
            ('head', 0),
            ('deprel', 'root'),
            ('deps', None),
            ('misc', None)]),
        children=[
            TreeNode(
                data=OrderedDict([
                    ('id', 1),
                    ('form', 'Jag'),
                    ('lemma', 'jag'),
                    ('upostag', 'PRON'),
                    ('xpostag', 'PRP'),
                    ('feats', OrderedDict([
                        ('Case', 'Nom'),
                        ('Definite', 'Def'),
                        ('Gender', 'Com'),
                        ('Number', 'Sing'),
                        ('PronType', 'Prs')
                    ])),
                    ('head', 2),
                    ('deprel', 'nsubj'),
                    ('deps', None),
                    ('misc', None)]),
                children=[]
            )
        ]
    )
]
