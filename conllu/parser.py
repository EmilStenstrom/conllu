from collections import OrderedDict

def parse(text):
    return list(
        [
            parse_line(line)
            for line in sentence.split("\n")
            if line and not line.strip().startswith("#")
        ]
        for sentence in text.split("\n\n")
        if sentence
    )

def parse_line(line):
    id_, form, lemma, upostag, xpostag, feats, head, deprel, deps, misc = \
        line.split("\t")

    return OrderedDict([
        ("id", parse_int_value(id_)),
        ("form", form),
        ("lemma", lemma),
        ("upostag", upostag),
        ("xpostag", parse_list_value(xpostag)),
        ("feats", parse_dict_value(feats)),
        ("head", parse_int_value(head)),
        ("deprel", deprel),
        ("deps", parse_nullable_value(deps)),
        ("misc", parse_dict_value(misc)),
    ])

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
