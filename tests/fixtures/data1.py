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
