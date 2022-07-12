import typing as T

from conllu.exceptions import ParseException

if T.TYPE_CHECKING:
    from conllu.models import TokenList


def serialize_field(field: T.Any) -> str:
    if field is None:
        return '_'

    if isinstance(field, dict):
        if field == {}:
            return '_'

        fields = []
        for key, value in field.items():
            if value is None:
                value = "_"
            if value == "":
                fields.append(key)
                continue

            fields.append('='.join((key, value)))

        return '|'.join(fields)

    if isinstance(field, tuple):
        return "".join([serialize_field(item) for item in field])

    if isinstance(field, list):
        if len(field[0]) != 2:
            raise ParseException("Can't serialize '{}', invalid format".format(field))
        return "|".join([serialize_field(value) + ":" + str(key) for key, value in field])

    return "{}".format(field)

def serialize(tokenlist: 'TokenList') -> str:
    lines = []

    if tokenlist.metadata:
        for key, value in tokenlist.metadata.items():
            if value:
                line = f"# {key} = {value}"
            else:
                line = f"# {key}"
            lines.append(line)

    for token_data in tokenlist:
        line = '\t'.join(serialize_field(val) for val in token_data.values())
        lines.append(line)

    return '\n'.join(lines) + "\n\n"
