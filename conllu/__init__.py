from __future__ import unicode_literals

import typing as T
from io import StringIO

from conllu.models import TokenList, TokenTree
from conllu.parser import (
    _FieldParserType, _MetadataParserType, parse_conllu_plus_fields, parse_sentences, parse_token_and_metadata,
)


def parse(data: str, fields: T.Optional[T.Sequence[str]] = None,
          field_parsers: T.Dict[str, _FieldParserType] = None,
          metadata_parsers: T.Optional[T.Dict[str, _MetadataParserType]] = None
          ) -> T.List[TokenList]:
    return list(parse_incr(
        StringIO(data),
        fields=fields,
        field_parsers=field_parsers,
        metadata_parsers=metadata_parsers
    ))

def parse_incr(in_file: T.TextIO, fields: T.Optional[T.Sequence[str]] = None,
               field_parsers: T.Dict[str, _FieldParserType] = None,
               metadata_parsers: T.Optional[T.Dict[str, _MetadataParserType]] = None
               ) -> T.Iterator[TokenList]:
    if not hasattr(in_file, 'read'):
        raise FileNotFoundError("Invalid file, 'parse_incr' needs an opened file as input")

    if not fields:
        fields = parse_conllu_plus_fields(in_file, metadata_parsers=metadata_parsers)

    for sentence in parse_sentences(in_file):
        yield TokenList(*parse_token_and_metadata(
            sentence,
            fields=fields,
            field_parsers=field_parsers,
            metadata_parsers=metadata_parsers
        ))

def parse_tree(data: str) -> T.List[TokenTree]:
    return list(parse_tree_incr(StringIO(data)))

def parse_tree_incr(in_file: T.TextIO) -> T.Iterator[TokenTree]:
    for tokenlist in parse_incr(in_file):
        yield tokenlist.to_tree()
