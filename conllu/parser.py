from __future__ import unicode_literals

import re
from collections import OrderedDict

from conllu.compat import fullmatch, text
from conllu.exceptions import ParseException
from conllu.models import Metadata, Token

DEFAULT_FIELDS = ('id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc')
DEFAULT_FIELD_PARSERS = {
    "id": lambda line, i: parse_id_value(line[i]),
    "xpos": lambda line, i: parse_nullable_value(line[i]),
    "feats": lambda line, i: parse_dict_value(line[i]),
    "head": lambda line, i: parse_int_value(line[i]),
    "deps": lambda line, i: parse_paired_list_value(line[i]),
    "misc": lambda line, i: parse_dict_value(line[i]),
}
DEFAULT_METADATA_PARSERS = {
    "newpar": lambda key, value: (key, value),
    "newdoc": lambda key, value: (key, value),
}

def parse_conllu_plus_fields(in_file, metadata_parsers=None):
    pos = in_file.tell()

    # Get first line
    try:
        first_sentence = next(parse_sentences(in_file))
        first_line = first_sentence.split("\n")[0]
    except StopIteration:
        first_line = ""

    # parse_sentences moves to file cursor, so reset it here
    in_file.seek(pos)

    if not first_line.startswith("#"):
        return

    _, metadata = parse_token_and_metadata(first_line, metadata_parsers=metadata_parsers)

    fields = None
    if "global.columns" in metadata and metadata["global.columns"]:
        fields = [value.lower() for value in metadata["global.columns"].split(" ")]

    return fields

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

def parse_token_and_metadata(data, fields=None, field_parsers=None, metadata_parsers=None):
    if not data:
        raise ParseException("Can't create TokenList, no data sent to constructor.")

    fields = fields or DEFAULT_FIELDS

    if not field_parsers:
        field_parsers = DEFAULT_FIELD_PARSERS.copy()
    elif sorted(field_parsers.keys()) != sorted(fields):
        new_field_parsers = DEFAULT_FIELD_PARSERS.copy()
        new_field_parsers.update(field_parsers)
        field_parsers = new_field_parsers

    tokens = []
    metadata = Metadata()

    for line in data.split('\n'):
        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            pairs = parse_comment_line(line, metadata_parsers=metadata_parsers)
            for key, value in pairs:
                metadata[key] = value
        else:
            tokens.append(parse_line(line, fields, field_parsers))

    return tokens, metadata

def parse_line(line, fields, field_parsers=None):
    # Be backwards compatible if people called parse_line without field_parsers before
    field_parsers = field_parsers or DEFAULT_FIELD_PARSERS

    # Support xpostag/upostag as aliases for xpos/upos (both ways)
    if "xpostag" not in field_parsers and "xpos" in field_parsers:
        field_parsers["xpostag"] = field_parsers["xpos"]
    if "xpos" not in field_parsers and "xpostag" in field_parsers:
        field_parsers["xpos"] = field_parsers["xpostag"]

    if "upostag" not in field_parsers and "upos" in field_parsers:
        field_parsers["upostag"] = field_parsers["upos"]
    if "upos" not in field_parsers and "upostag" in field_parsers:
        field_parsers["upos"] = field_parsers["upostag"]

    line = re.split(r"\t| {2,}", line)

    if len(line) == 1:
        raise ParseException("Invalid line format, line must contain either tabs or two spaces.")

    data = Token()

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

        data[text(field)] = value

    return data

def parse_comment_line(line, metadata_parsers=None):
    line = line.strip()

    if line[0] != '#':
        raise ParseException("Invalid comment format, comment must start with '#'")

    key, value = parse_pair_value(line[1:])

    if not metadata_parsers:
        metadata_parsers = DEFAULT_METADATA_PARSERS.copy()
    else:
        new_metadata_parsers = DEFAULT_METADATA_PARSERS.copy()
        new_metadata_parsers.update(metadata_parsers)
        metadata_parsers = new_metadata_parsers

    custom_result = None
    if key in metadata_parsers:
        custom_result = metadata_parsers[key](key, value)
    elif "__fallback__" in metadata_parsers:
        custom_result = metadata_parsers["__fallback__"](key, value)

    # Allow returning pair instead of list of pairs from metadata parsers
    if custom_result:
        if isinstance(custom_result, tuple):
            key, value = custom_result
            return [(text(key), value)]
        return [(text(key), value) for key, value in custom_result]

    if not key or not value:
        # Lines without value are invalid by default
        return []

    return [(text(key), value)]

def parse_pair_value(value):
    key_maybe_value = value.split('=', 1)
    key = key_maybe_value[0].strip()
    value = None if len(key_maybe_value) == 1 else key_maybe_value[1].strip()

    return key, value


INTEGER = re.compile(r"0|(\-?[1-9][0-9]*)")

def parse_int_value(value):
    if value == '_':
        return None

    if fullmatch(INTEGER, value):
        return int(value)
    else:
        raise ParseException("'{}' is not a valid value for parse_int_value.".format(value))


ID_SINGLE = re.compile(r"(?:0|[1-9][0-9]*)")
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
DEPS_RE = re.compile("(" + ANY_ID.pattern + r")(:[^\d:_\-|][^:|]*)+")
MULTI_DEPS_PATTERN = re.compile(r"{}(\|{})*".format(DEPS_RE.pattern, DEPS_RE.pattern))

def parse_paired_list_value(value):
    if fullmatch(MULTI_DEPS_PATTERN, value):
        return [
            (part.split(":", 1)[1], parse_id_value(part.split(":")[0]))
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

# DEPRECATED: Mantain old paths until next major version

def serialize(*args, **kwargs):
    from conllu.serializer import serialize as new_serialize
    return new_serialize(*args, **kwargs)

def serialize_field(*args, **kwargs):
    from conllu.serializer import serialize_field as new_serialize_field
    return new_serialize_field(*args, **kwargs)

def head_to_token(*args, **kwargs):
    from conllu.models import TokenList
    return TokenList.head_to_token(*args, **kwargs)
