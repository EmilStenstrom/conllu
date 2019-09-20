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

    """),

    dedent("""\
        # sent_id = weblog-blogspot.com_healingiraq_20040409053012_ENG_20040409_053012-0022
        # text = Over 300 Iraqis are reported dead and 500 wounded in Fallujah alone.
        1\tOver\tover\tADV\tRB\t_\t2\tadvmod\t2:advmod\t_
        2\t300\t300\tNUM\tCD\tNumType=Card\t3\tnummod\t3:nummod\t_
        3\tIraqis\tIraqis\tPROPN\tNNPS\tNumber=Plur\t5\tnsubj:pass\t5:nsubj:pass|6:nsubj:xsubj|8:nsubj:pass\t_
        4\tare\tbe\tAUX\tVBP\tMood=Ind|Tense=Pres|VerbForm=Fin\t5\taux:pass\t5:aux:pass\t_
        5\treported\treport\tVERB\tVBN\tTense=Past|VerbForm=Part|Voice=Pass\t0\troot\t0:root\t_
        6\tdead\tdead\tADJ\tJJ\tDegree=Pos\t5\txcomp\t5:xcomp\t_
        7\tand\tand\tCCONJ\tCC\t_\t8\tcc\t8:cc|8.1:cc\t_
        8\t500\t500\tNUM\tCD\tNumType=Card\t5\tconj\t5:conj:and|8.1:nsubj:pass|9:nsubj:xsubj\t_
        8.1\treported\treport\tVERB\tVBN\tTense=Past|VerbForm=Part|Voice=Pass\t_\t_\t5:conj:and\tCopyOf=5
        9\twounded\twounded\tADJ\tJJ\tDegree=Pos\t8\torphan\t8.1:xcomp\t_
        10\tin\tin\tADP\tIN\t_\t11\tcase\t11:case\t_
        11\tFallujah\tFallujah\tPROPN\tNNP\tNumber=Sing\t5\tobl\t5:obl:in\t_
        12\talone\talone\tADV\tRB\t_\t11\tadvmod\t11:advmod\tSpaceAfter=No
        13\t.\t.\tPUNCT\t.\t_\t5\tpunct\t5:punct\t_

    """)
]
