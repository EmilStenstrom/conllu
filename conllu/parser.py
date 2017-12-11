import re
from collections import OrderedDict, defaultdict
from conllu.tree_helpers import create_tree

DEFAULT_FIELDS = ('id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc')

def parse(text, fields=DEFAULT_FIELDS):
    return [
        [
            parse_line(line, fields)
            for line in sentence.split("\n")
            if line and not line.strip().startswith("#")
        ]
        for sentence in text.split("\n\n")
        if sentence
    ]

def parse_tree(text):
    result = parse(text)

    trees = []
    for sentence in result:

        head_indexed = defaultdict(list)
        for token in sentence:
            head_indexed[token["head"]].append(token)

        trees += create_tree(head_indexed)

    return trees

def parse_line(line, fields=DEFAULT_FIELDS):
    line = re.split(r"\t| {2,}", line)
    data = OrderedDict()

    for i, field in enumerate(fields):
        # Allow parsing CoNNL-U files with fewer columns
        if i >= len(line):
            break

        if field == "id":
            value = parse_int_value(line[i])

        elif field == "xpostag":
            value = parse_nullable_value(line[i])

        elif field == "feats":
            value = parse_dict_value(line[i])

        elif field == "head":
            value = parse_int_value(line[i])

        elif field == "deps":
            value = parse_nullable_value(line[i])

        elif field == "misc":
            value = parse_dict_value(line[i])

        else:
            value = line[i]

        data[field] = value

    return data

def parse_int_value(value):
    if value.isdigit():
        return int(value)

    return None

def parse_dict_value(value):
    if "=" in value:
        return OrderedDict([
            (part.split("=")[0], parse_nullable_value(part.split("=")[1]))
            for part in value.split("|")
        ])

    return parse_nullable_value(value)

def parse_nullable_value(value):
    if not value or value == "_":
        return None

    return value

def serialize_field(field):
    if field is None:
        return '_'

    if isinstance(field, OrderedDict):
        serialized_fields = []
        for key_value in field.items():
            serialized_fields.append('='.join(key_value))

        return '|'.join(serialized_fields)

    return str(field)

def serialize_tree(root):
    def add_subtree(root_token, token_list):
        for child_token in root_token.children:
            token_list = add_subtree(child_token, token_list)

        token_list.append(root_token.data)
        return token_list

    tokens = []
    add_subtree(root, tokens)

    sorted_tokens = sorted(tokens, key=lambda t: t['id'])
    lines = []
    for token_data in sorted_tokens:
        line = '\t'.join(serialize_field(val) for val in token_data.values())
        lines.append(line)

    text = '\n'.join(lines)
    return text
