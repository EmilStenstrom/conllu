from collections import OrderedDict, defaultdict
from conllu.tree_helpers import create_tree

def parse(text, to_parse=['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']):
    '''
    to_parse - a list of columns to parse (id, form, lemma, upostag, xpostag, feats, head, deprel, deps or misc).
    '''
    return list(
        [
            parse_line(line, to_parse)
            for line in sentence.split("\n")
            if line and not line.strip().startswith("#")
        ]
        for sentence in text.split("\n\n")
        if sentence
    )

def parse_tree(text):
    result = parse(text)

    trees = []
    for sentence in result:

        head_indexed = defaultdict(list)
        for token in sentence:
            head_indexed[token["head"]].append(token)

        trees += create_tree(head_indexed)

    return trees

def parse_line(line, to_parse):
    spl_line = line.split("\t")
    d = OrderedDict()
    if len(spl_line) == len(to_parse):
        for i in range(len(to_parse)):
            d[to_parse[i]] = spl_line[i]
        if "id" in to_parse:
            d["id"] = parse_int_value(d["id"])
        if "xpostag" in to_parse:
            d["xpostag"] = parse_list_value(d["xpostag"])
        if "feats" in to_parse:
            d["feats"] = parse_dict_value(d["feats"])
        if "head" in to_parse:
            d["head"] = parse_int_value(d["head"])
        if "deps" in to_parse:
            d["deps"] = parse_nullable_value(d["deps"])
        if "misc" in to_parse:
            d["misc"] = parse_dict_value(d["misc"])
    else:
        print('Enter a correct number of columns')
    return d

def parse_int_value(value):
    if value.isdigit():
        return int(value)

    return None

def parse_list_value(value):
    if "|" in value:
        return [parse_nullable_value(part) for part in value.split("|")]

    return parse_nullable_value(value)

def parse_dict_value(value):
    if "=" in value:
        return OrderedDict([
            (part.split("=")[0], parse_nullable_value(part.split("=")[1]))
            for part in value.split("|")
        ])

    return parse_nullable_value(value)

def parse_nullable_value(value):
    if value == "_":
        return None

    return value
