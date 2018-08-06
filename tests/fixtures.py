# coding: utf-8
from __future__ import unicode_literals

from textwrap import dedent

TESTCASES = [
    # To appear (EMNLP 2014): Detecting Non-compositional MWE Components using Wiktionary
    # http://people.eng.unimelb.edu.au/tbaldwin/pubs/emnlp2014-mwe.pdf … #nlproc
    dedent("""\
        1\tTo\t_\tP\tP\t_\t0\t_
        2\tappear\t_\tV\tV\t_\t1\t_
        3\t(\t_\t,\t,\t_\t-1\t_
        4\tEMNLP\t_\t^\t^\t_\t0\t_
        5\t2014\t_\t$\t$\t_\t4\tMWE
        6\t):\t_\t,\t,\t_\t-1\t_
        7\tDetecting\t_\tV\tV\t_\t11\t_
        8\tNon-compositional\t_\t^\t^\t_\t10\tMWE
        9\tMWE\t_\t^\t^\t_\t10\tMWE
        10\tComponents\t_\t^\t^\t_\t11\t_
        11\tusing\t_\tV\tV\t_\t0\t_
        12\tWiktionary\t_\tN\tN\t_\t11\t_
        13\thttp://people.eng.unimelb.edu.au/tbaldwin/pubs/emnlp2014-mwe.pdf\t_\tU\tU\t_\t-1\t_
        14\t…\t_\t,\t,\t_\t-1\t_
        15\t#nlproc\t_\t#\t#\t_\t-1\t_

    """),

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
