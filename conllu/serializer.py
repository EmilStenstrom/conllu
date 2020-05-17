from __future__ import unicode_literals

from collections import OrderedDict

from conllu.compat import text
from conllu.exceptions import ParseException


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
            if value:
                line = "# " + key + " = " + value
            else:
                line = "# " + key
            lines.append(line)

    for token_data in tokenlist:
        line = '\t'.join(serialize_field(val) for val in token_data.values())
        lines.append(line)

    return '\n'.join(lines) + "\n\n"
