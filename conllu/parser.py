from __future__ import unicode_literals

import re
from collections import OrderedDict, defaultdict

from conllu.tree_helpers import create_tree

DEFAULT_FIELDS = ('id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc')

deps_pattern = r"\d+:[a-z][a-z_-]*(:[a-z][a-z_-]*)?"
MULTI_DEPS_PATTERN = re.compile(r"^{}(\|{})*$".format(deps_pattern, deps_pattern))

class ParseException(Exception):
    pass

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

def sent_to_tree(sentence):
    head_indexed = defaultdict(list)
    for token in sentence:
        # If HEAD is negative, treat it as child of the root node
        head = max(token["head"] or 0, 0)
        head_indexed[head].append(token)

    return create_tree(head_indexed)

def parse_tree(text):
    result = parse(text)

    if "head" not in result[0][0]:
        raise ParseException("Can't parse tree, missing 'head' field.")

    trees = []
    for sentence in result:
        trees += sent_to_tree(sentence)

    return trees

def parse_line(line, fields=DEFAULT_FIELDS):
    line = re.split(r"\t| {2,}", line)

    if len(line) == 1 and " " in line[0]:
        raise ParseException("Invalid line format, line must contain either tabs or two spaces.")

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
            value = parse_paired_list_value(line[i])

        elif field == "misc":
            value = parse_dict_value(line[i])

        else:
            value = line[i]

        data[field] = value

    return data

def parse_int_value(value):
    if value == '_':
        return None
    try:
        return int(value)
    except ValueError:
        return None

def parse_paired_list_value(value):
    if re.match(MULTI_DEPS_PATTERN, value):
        return [
            (part.split(":", 1)[1], parse_int_value(part.split(":", 1)[0]))
            for part in value.split("|")
        ]

    return parse_nullable_value(value)

def parse_dict_value(value):
    if "=" in value:
        return OrderedDict([
            (part.split("=")[0], parse_nullable_value(part.split("=")[1]))
            for part in value.split("|") if len(part.split('=')) == 2
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

    return "{}".format(field)

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
