# encoding: utf-8
from __future__ import unicode_literals
from textwrap import dedent

# The quick brown fox jumps over the lazy dog
data1 = dedent("""
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

""")

# Då var han elva år.
data2 = dedent("""
    1    Då      då     ADV      AB                    _
    2    var     vara   VERB     VB.PRET.ACT           Tense=Past|Voice=Act
    3    han     han    PRON     PN.UTR.SIN.DEF.NOM    Case=Nom|Definite=Def|Gender=Com|Number=Sing
    4    elva    elva   NUM      RG.NOM                Case=Nom|NumType=Card
    5    år      år     NOUN     NN.NEU.PLU.IND.NOM    Case=Nom|Definite=Ind|Gender=Neut|Number=Plur
    6    .       .      PUNCT    DL.MAD                _

""")

# They buy and sell books
data3 = dedent("""
    1    They     they    PRON    PRP    Case=Nom|Number=Plur               2    nsubj    2:nsubj|4:nsubj
    2    buy      buy     VERB    VBP    Number=Plur|Person=3|Tense=Pres    0    root     0:root
    3    and      and     CONJ    CC     _                                  4    cc       4:cc
    4    sell     sell    VERB    VBP    Number=Plur|Person=3|Tense=Pres    2    conj     0:root|2:conj
    5    books    book    NOUN    NNS    Number=Plur                        2    obj      2:obj|4:obj
    6    .        .       PUNCT   .      _                                  2    punct    2:punct
""")

data4 = dedent("""
    # sent_id = 1
    # text = They buy and sell books.
    1   They     they    PRON    PRP    Case=Nom|Number=Plur               2   nsubj   2:nsubj|4:nsubj   _
    2   buy      buy     VERB    VBP    Number=Plur|Person=3|Tense=Pres    0   root    0:root            _
    3   and      and     CONJ    CC     _                                  4   cc      4:cc              _
    4   sell     sell    VERB    VBP    Number=Plur|Person=3|Tense=Pres    2   conj    0:root|2:conj     _
    5   books    book    NOUN    NNS    Number=Plur                        2   obj     2:obj|4:obj       SpaceAfter=No
    6   .        .       PUNCT   .      _                                  2   punct   2:punct           _

    # sent_id = 2
    # text = I have no clue.
    1   I       I       PRON    PRP   Case=Nom|Number=Sing|Person=1     2   nsubj   _   _
    2   have    have    VERB    VBP   Number=Sing|Person=1|Tense=Pres   0   root    _   _
    3   no      no      DET     DT    PronType=Neg                      4   det     _   _
    4   clue    clue    NOUN    NN    Number=Sing                       2   obj     _   SpaceAfter=No
    5   .       .       PUNCT   .     _                                 2   punct   _   _

""")

data5 = dedent("""
    1	Jag	jag	PRON	PRP	Case=Nom|Definite=Def|Gender=Com|Number=Sing|PronType=Prs	2	nsubj	_	_
    2	längtar	längta	VERB	VBP	Mood=Ind|Tense=Pres|VerbForm=Fin|Voice=Act	0	root	_	_

""")
