from __future__ import unicode_literals

import re
from collections import OrderedDict, defaultdict

from conllu.compat import fullmatch, text

DEFAULT_FIELDS = ('id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc')
DEFAULT_FIELD_PARSERS = {
    "id": lambda line, i: parse_id_value(line[i]),
    "xpostag": lambda line, i: parse_nullable_value(line[i]),
    "feats": lambda line, i: parse_dict_value(line[i]),
    "head": lambda line, i: parse_int_value(line[i]),
    "deps": lambda line, i: parse_paired_list_value(line[i]),
    "misc": lambda line, i: parse_dict_value(line[i]),
}

def parse_sentences(in_file):
    buf = []
    for line in in_file:
        if line == "\n":
            if not buf:
                continue
            yield "".join(buf).rstrip()
            buf = []
        else:
            buf.append(line)
    if buf:
        yield "".join(buf).rstrip()

def parse_token_and_metadata(data, fields=None, field_parsers=None):
    if not data:
        raise ParseException("Can't create TokenList, no data sent to constructor.")

    fields = fields or DEFAULT_FIELDS
    field_parsers = field_parsers or DEFAULT_FIELD_PARSERS

    tokens = []
    metadata = OrderedDict()

    for line in data.split('\n'):
        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            var_name, var_value = parse_comment_line(line)
            if var_name:
                metadata[var_name] = var_value
        else:
            tokens.append(parse_line(line, fields, field_parsers))

    return tokens, metadata

def parse_line(line, fields, field_parsers=None):
    # Be backwards compatible if people called parse_line without field_parsers before
    field_parsers = field_parsers or DEFAULT_FIELD_PARSERS

    line = re.split(r"\t| {2,}", line)

    if len(line) == 1 and " " in line[0]:
        raise ParseException("Invalid line format, line must contain either tabs or two spaces.")

    data = OrderedDict()

    for i, field in enumerate(fields):
        # Allow parsing CoNNL-U files with fewer columns
        if i >= len(line):
            break

        if field in field_parsers:
            try:
                value = field_parsers[field](line, i)
            except ParseException as e:
                raise ParseException("Failed parsing field '{}': ".format(field) + str(e))

        else:
            value = line[i]

        data[field] = value

    return data

def parse_comment_line(line):
    line = line.strip()

    if line[0] != '#':
        raise ParseException("Invalid comment format, comment must start with '#'")

    stripped = line[1:].strip()
    if '=' not in line and stripped != 'newdoc' and stripped != 'newpar':
        return None, None

    name_value = line[1:].split('=', 1)
    var_name = name_value[0].strip()
    var_value = None if len(name_value) == 1 else name_value[1].strip()

    return var_name, var_value


INTEGER = re.compile(r"0|(\-?[1-9][0-9]*)")

def parse_int_value(value):
    if value == '_':
        return None

    if fullmatch(INTEGER, value):
        return int(value)
    else:
        raise ParseException("'{}' is not a valid value for parse_int_value.".format(value))


ID_SINGLE = re.compile(r"[1-9][0-9]*")
ID_RANGE = re.compile(r"[1-9][0-9]*\-[1-9][0-9]*")
ID_DOT_ID = re.compile(r"[0-9][0-9]*\.[1-9][0-9]*")

def parse_id_value(value):
    if not value or value == '_':
        return None

    if fullmatch(ID_SINGLE, value):
        return int(value)

    elif fullmatch(ID_RANGE, value):
        from_, to = value.split("-")
        from_, to = int(from_), int(to)
        if to > from_:
            return (int(from_), "-", int(to))

    elif fullmatch(ID_DOT_ID, value):
        return (int(value.split(".")[0]), ".", int(value.split(".")[1]))

    raise ParseException("'{}' is not a valid ID.".format(value))


ANY_ID = re.compile(ID_SINGLE.pattern + "|" + ID_RANGE.pattern + "|" + ID_DOT_ID.pattern)
DEPS_RE = re.compile("(" + ANY_ID.pattern + r"):[a-z][a-z_-]*(\:[a-z][a-z_-]*)?")
MULTI_DEPS_PATTERN = re.compile(r"{}(\|{})*".format(DEPS_RE.pattern, DEPS_RE.pattern))

def parse_paired_list_value(value):
    if fullmatch(MULTI_DEPS_PATTERN, value):
        return [
            (part.split(":", 1)[1], parse_id_value(part.split(":", 1)[0]))
            for part in value.split("|")
        ]

    return parse_nullable_value(value)

def parse_dict_value(value):
    if parse_nullable_value(value) is None:
        return None

    return OrderedDict([
        (part.split("=")[0], parse_nullable_value(part.split("=")[1]) if "=" in part else "")
        for part in value.split("|") if parse_nullable_value(part.split("=")[0]) is not None
    ])

def parse_nullable_value(value):
    if not value or value == "_":
        return None

    return value

def head_to_token(sentence):
    if not sentence:
        raise ParseException("Can't parse tree, need a tokenlist as input.")

    if "head" not in sentence[0]:
        raise ParseException("Can't parse tree, missing 'head' field.")

    head_indexed = defaultdict(list)
    for token in sentence:
        # Filter out range and decimal ID:s before building tree
        if "id" in token and not isinstance(token["id"], int):
            continue

        # Filter out tokens with negative head, they are sometimes used to
        # specify tokens which should not be included in tree
        if token["head"] < 0:
            continue

        head_indexed[token["head"]].append(token)

    if len(head_indexed[0]) == 0:
        raise ParseException("Found no head node, can't build tree")

    if len(head_indexed[0]) > 1:
        raise ParseException("Can't parse tree, found multiple root nodes.")

    return head_indexed

def serialize_field(field):
    if field is None:
        return '_'

    if isinstance(field, OrderedDict):
        fields = []
        for key, value in field.items():
            if value is None:
                value = "_"

            fields.append('='.join((key, value)))

        return '|'.join(fields)

    if isinstance(field, tuple):
        return "".join([serialize_field(item) for item in field])

    if isinstance(field, list):
        if len(field[0]) != 2:
            raise ParseException("Can't serialize '{}', invalid format".format(field))
        return "|".join([serialize_field(value) + ":" + text(key) for key, value in field])

    return "{}".format(field)

def serialize(tokenlist):
    lines = []

    if tokenlist.metadata:
        for key, value in tokenlist.metadata.items():
            line = "# " + key + " = " + value
            lines.append(line)

    for token_data in tokenlist:
        line = '\t'.join(serialize_field(val) for val in token_data.values())
        lines.append(line)

    return '\n'.join(lines) + "\n\n"

class ParseException(Exception):
    pass
