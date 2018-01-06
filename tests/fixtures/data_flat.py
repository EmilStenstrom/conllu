# encoding: utf-8
from __future__ import unicode_literals
from collections import OrderedDict

data1_flat = [[
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

data2_flat = [[
    OrderedDict([
        ('id', 1),
        ('form', 'Då'),
        ('lemma', 'då'),
        ('upostag', 'ADV'),
        ('xpostag', 'AB'),
        ('feats', None)
    ]), OrderedDict([
        ('id', 2),
        ('form', 'var'),
        ('lemma', 'vara'),
        ('upostag', 'VERB'),
        ('xpostag', 'VB.PRET.ACT'),
        ('feats', OrderedDict([('Tense', 'Past'), ('Voice', 'Act')]))
    ]), OrderedDict([
        ('id', 3),
        ('form', 'han'),
        ('lemma', 'han'),
        ('upostag', 'PRON'),
        ('xpostag', 'PN.UTR.SIN.DEF.NOM'),
        ('feats', OrderedDict([
            ('Case', 'Nom'),
            ('Definite', 'Def'),
            ('Gender', 'Com'),
            ('Number', 'Sing')
        ]))
    ]), OrderedDict([
        ('id', 4),
        ('form', 'elva'),
        ('lemma', 'elva'),
        ('upostag', 'NUM'),
        ('xpostag', 'RG.NOM'),
        ('feats', OrderedDict([('Case', 'Nom'), ('NumType', 'Card')]))
    ]), OrderedDict([
        ('id', 5),
        ('form', 'år'),
        ('lemma', 'år'),
        ('upostag', 'NOUN'),
        ('xpostag', 'NN.NEU.PLU.IND.NOM'),
        ('feats', OrderedDict([
            ('Case', 'Nom'),
            ('Definite', 'Ind'),
            ('Gender', 'Neut'),
            ('Number', 'Plur')
        ]))
    ]), OrderedDict([
        ('id', 6),
        ('form', '.'),
        ('lemma', '.'),
        ('upostag', 'PUNCT'),
        ('xpostag', 'DL.MAD'),
        ('feats', None)
    ])
]]

data3_flat = [[
    OrderedDict([
        ('id', 1),
        ('form', 'They'),
        ('lemma', 'they'),
        ('upostag', 'PRON'),
        ('xpostag', 'PRP'),
        ('feats', OrderedDict([
            ('Case', 'Nom'),
            ('Number', 'Plur')
        ])),
        ('head', 2),
        ('deprel', 'nsubj'),
        ('deps', [
            ('nsubj', 2),
            ('nsubj', 4)
        ])
    ]),
    OrderedDict([
        ('id', 2),
        ('form', 'buy'),
        ('lemma', 'buy'),
        ('upostag', 'VERB'),
        ('xpostag', 'VBP'),
        ('feats', OrderedDict([
            ('Number', 'Plur'),
            ('Person', '3'),
            ('Tense', 'Pres')
        ])),
        ('head', 0),
        ('deprel', 'root'),
        ('deps', [
            ('root', 0)
        ])
    ]),
    OrderedDict([
        ('id', 3),
        ('form', 'and'),
        ('lemma', 'and'),
        ('upostag', 'CONJ'),
        ('xpostag', 'CC'),
        ('feats', None),
        ('head', 4),
        ('deprel', 'cc'),
        ('deps', [
            ('cc', 4)
        ])
    ]),
    OrderedDict([
        ('id', 4),
        ('form', 'sell'),
        ('lemma', 'sell'),
        ('upostag', 'VERB'),
        ('xpostag', 'VBP'),
        ('feats', OrderedDict([
            ('Number', 'Plur'),
            ('Person', '3'),
            ('Tense', 'Pres')
        ])),
        ('head', 2),
        ('deprel', 'conj'),
        ('deps', [
            ('root', 0),
            ('conj', 2)
        ])
    ]),
    OrderedDict([
        ('id', 5),
        ('form', 'books'),
        ('lemma', 'book'),
        ('upostag', 'NOUN'),
        ('xpostag', 'NNS'),
        ('feats', OrderedDict([
            ('Number', 'Plur')
        ])),
        ('head', 2),
        ('deprel', 'obj'),
        ('deps', [
            ('obj', 2),
            ('obj', 4)
        ])
    ]),
    OrderedDict([
        ('id', 6),
        ('form', '.'),
        ('lemma', '.'),
        ('upostag', 'PUNCT'),
        ('xpostag', '.'),
        ('feats', None),
        ('head', 2),
        ('deprel', 'punct'),
        ('deps', [
            ('punct', 2)
        ])
    ])
]]

data4_flat = [
    [
        OrderedDict([
            ('id', 1),
            ('form', 'They'),
            ('lemma', 'they'),
            ('upostag', 'PRON'),
            ('xpostag', 'PRP'),
            ('feats', OrderedDict([
                ('Case', 'Nom'),
                ('Number', 'Plur')
            ])),
            ('head', 2),
            ('deprel', 'nsubj'),
            ('deps', [
                ('nsubj', 2),
                ('nsubj', 4)
            ]),
            ('misc', None)
        ]),
        OrderedDict([
            ('id', 2),
            ('form', 'buy'),
            ('lemma', 'buy'),
            ('upostag', 'VERB'),
            ('xpostag', 'VBP'),
            ('feats', OrderedDict([
                ('Number', 'Plur'),
                ('Person', '3'),
                ('Tense', 'Pres')
            ])),
            ('head', 0),
            ('deprel', 'root'),
            ('deps', [
                ('root', 0)
            ]),
            ('misc', None)
        ]),
        OrderedDict([
            ('id', 3),
            ('form', 'and'),
            ('lemma', 'and'),
            ('upostag', 'CONJ'),
            ('xpostag', 'CC'),
            ('feats', None),
            ('head', 4),
            ('deprel', 'cc'),
            ('deps', [
                ('cc', 4)
            ]),
            ('misc', None)
        ]),
        OrderedDict([
            ('id', 4),
            ('form', 'sell'),
            ('lemma', 'sell'),
            ('upostag', 'VERB'),
            ('xpostag', 'VBP'),
            ('feats', OrderedDict([
                ('Number', 'Plur'),
                ('Person', '3'),
                ('Tense', 'Pres')
            ])),
            ('head', 2),
            ('deprel', 'conj'),
            ('deps', [
                ('root', 0),
                ('conj', 2)
            ]),
            ('misc', None)
        ]),
        OrderedDict([
            ('id', 5),
            ('form', 'books'),
            ('lemma', 'book'),
            ('upostag', 'NOUN'),
            ('xpostag', 'NNS'),
            ('feats', OrderedDict([
                ('Number', 'Plur')
            ])),
            ('head', 2),
            ('deprel', 'obj'),
            ('deps', [
                ('obj', 2),
                ('obj', 4)
            ]),
            ('misc', OrderedDict([
                ('SpaceAfter', 'No')
            ]))
        ]),
        OrderedDict([
            ('id', 6),
            ('form', '.'),
            ('lemma', '.'),
            ('upostag', 'PUNCT'),
            ('xpostag', '.'),
            ('feats', None),
            ('head', 2),
            ('deprel', 'punct'),
            ('deps', [
                ('punct', 2)
            ]),
            ('misc', None)
        ])
    ],
    [
        OrderedDict([
            ('id', 1),
            ('form', 'I'),
            ('lemma', 'I'),
            ('upostag', 'PRON'),
            ('xpostag', 'PRP'),
            ('feats', OrderedDict([
                ('Case', 'Nom'),
                ('Number', 'Sing'),
                ('Person', '1')
            ])),
            ('head', 2),
            ('deprel', 'nsubj'),
            ('deps', None),
            ('misc', None)
        ]),
        OrderedDict([
            ('id', 2),
            ('form', 'have'),
            ('lemma', 'have'),
            ('upostag', 'VERB'),
            ('xpostag', 'VBP'),
            ('feats', OrderedDict([
                ('Number', 'Sing'),
                ('Person', '1'),
                ('Tense', 'Pres')
            ])),
            ('head', 0),
            ('deprel', 'root'),
            ('deps', None),
            ('misc', None)
        ]),
        OrderedDict([
            ('id', 3),
            ('form', 'no'),
            ('lemma', 'no'),
            ('upostag', 'DET'),
            ('xpostag', 'DT'),
            ('feats', OrderedDict([
                ('PronType', 'Neg')
            ])),
            ('head', 4),
            ('deprel', 'det'),
            ('deps', None),
            ('misc', None)
        ]),
        OrderedDict([
            ('id', 4),
            ('form', 'clue'),
            ('lemma', 'clue'),
            ('upostag', 'NOUN'),
            ('xpostag', 'NN'),
            ('feats', OrderedDict([
                ('Number', 'Sing')
            ])),
            ('head', 2),
            ('deprel', 'obj'),
            ('deps', None),
            ('misc', OrderedDict([
                ('SpaceAfter', 'No')
            ]))
        ]),
        OrderedDict([
            ('id', 5),
            ('form', '.'),
            ('lemma', '.'),
            ('upostag', 'PUNCT'),
            ('xpostag', '.'),
            ('feats', None),
            ('head', 2),
            ('deprel', 'punct'),
            ('deps', None),
            ('misc', None)
        ])
    ]
]
