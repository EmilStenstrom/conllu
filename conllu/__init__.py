import typing as T
from io import StringIO

from conllu.models import Metadata, SentenceGenerator, SentenceList, Token, TokenList, TokenTree
from conllu.parser import (
    DEFAULT_FIELDS, _FieldParserType, _MetadataParserType, parse_sentences, parse_token_and_metadata,
)

__all__ = [
    "parse", "parse_incr", "parse_tree", "parse_tree_incr",
    "SentenceGenerator", "SentenceList", "TokenList", "TokenTree", "Token", "Metadata",
    "parse_sentences", "parse_token_and_metadata",
]

def parse(data: str, fields: T.Optional[T.Sequence[str]] = None,
          field_parsers: T.Optional[T.Dict[str, _FieldParserType]] = None,
          metadata_parsers: T.Optional[T.Dict[str, _MetadataParserType]] = None
          ) -> SentenceList:
    return SentenceList(parse_incr(
        StringIO(data),
        fields=fields,
        field_parsers=field_parsers,
        metadata_parsers=metadata_parsers
    ))

def parse_incr(in_file: T.TextIO, fields: T.Optional[T.Sequence[str]] = None,
               field_parsers: T.Optional[T.Dict[str, _FieldParserType]] = None,
               metadata_parsers: T.Optional[T.Dict[str, _MetadataParserType]] = None
               ) -> SentenceGenerator:

    if not hasattr(in_file, 'read'):
        raise FileNotFoundError("Invalid file, 'parse_incr' needs an opened file as input")

    def generator():
        global_columns = None

        for sentence in parse_sentences(in_file):
            lines = sentence.strip().split('\n')
            current_metadata = [line for line in lines if line.startswith('#')]
            current_sentence = [line for line in lines if not line.startswith('#')]

            if any(line.startswith('# global.columns = ') for line in current_metadata):
                global_columns = next(
                    line.split('=', 1)[1].strip().split()
                    for line in current_metadata if line.startswith('# global.columns = ')
                )

            used_fields = global_columns if global_columns else (fields if fields else DEFAULT_FIELDS)
            used_fields = [field.lower() for field in used_fields]

            yield parse_token_and_metadata(
                '\n'.join(current_metadata + current_sentence),
                fields=used_fields,
                field_parsers=field_parsers,
                metadata_parsers=metadata_parsers
            )

    return SentenceGenerator(generator())

def parse_tree(data: str) -> T.List[TokenTree]:
    return list(parse_tree_incr(StringIO(data)))

def parse_tree_incr(in_file: T.TextIO) -> T.Iterator[TokenTree]:
    for tokenlist in parse_incr(in_file):
        yield tokenlist.to_tree()
