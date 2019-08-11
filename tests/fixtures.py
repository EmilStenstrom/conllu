# coding: utf-8
from __future__ import unicode_literals

from textwrap import dedent

TESTCASES = [
    # example taken from arabic UD2.0
    # sent_id = ummah.20040705.0014:p6u1
    # removed not needed words
    dedent("""\
        1-2\tويشارك\t_\t_\t_\t_\t_\t_\t_\t_
        1\tو\tوَ\tCCONJ\tC---------\t_\t0\troot\t_\tVform=وَ|Gloss=and|Root=wa|Translit=wa|LTranslit=wa
        19\tآلافكار\tآلافكار\tX\tU---------\t_\t1\tnmod\t_\tVform=آلافكار|Translit=lAfkAr

    """),

    # example taken from ru_syntagrus UD2.0
    # 2003Anketa.xml 45
    dedent("""\
        1\t-\t-\tPUNCT\t_\t_\t2\tpunct\t2:punct\t_
        2\tЯ\tя\tPRON\t_\tCase=Nom|Number=Sing|Person=1\t4\tnsubj\t2.1:nsubj\t_
        2.1\t_\t_\t_\t_\t_\t_\t_\t0:exroot\t_
        3\tнасчет\tнасчет\tADP\t_\t_\t4\tcase\t4:case\t_
        4\tработы\tработа\tNOUN\t_\tAnimacy=Inan|Case=Gen|Gender=Fem|Number=Sing\t0\troot\t0:root\tSpaceAfter=No
        5\t…\t…\tPUNCT\t_\t_\t4\tpunct\t4:punct\t_

    """)
]

TESTCASES_CONLL2009 = [
    dedent("""\
        #\tid\tform\tlemma\tplemma\tpos\tppos\tfeats\tpfeats\thead\tphead\tdeprel\tpdeprel\tfillpred\tpred\tapreds
        1\tZ\tz\tz\tR\tR\tSubPOS=R|Cas=2\tSubPOS=R|Cas=2\t10\t10\tAuxP\tAuxP\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_
        2\ttéto\ttento\ttento\tP\tP\tSubPOS=D|Gen=F|Num=S|Cas=2\tSubPOS=D|Gen=F|Num=S|Cas=2\t3\t3\tAtr\tAtr\tY\ttento\t_\tRSTR\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_\t_
        3\tknihy\tkniha\tkniha\tN\tN\tSubPOS=N|Gen=F|Num=S|Cas=2|Neg=A\tSubPOS=N|Gen=F|Num=S|Cas=2|Neg=A\t1\t1\tAdv\tAdv\tY\tkniha\t_\t_\t_\t_\t_\t_\t_\tDIR1\t_\t_\t_\t_\t_\t_\t_\t_

    """)
]
