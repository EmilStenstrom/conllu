import typing as T
from collections import defaultdict
from collections.abc import Mapping

from conllu.exceptions import ParseException
from conllu.serializer import serialize

DEFAULT_EXCLUDE_FIELDS = ('id', 'deprel', 'xpos', 'feats', 'head', 'deps', 'misc')

if T.TYPE_CHECKING:
    class SupportsIndex(T.Protocol):
        def __index__(self) -> int:
            pass

    class SupportsNext(T.Protocol):
        def __next__(self) -> int:
            pass

class Metadata(dict):
    pass

class Token(dict):
    MAPPING = {
        "upostag": "upos",
        "xpostag": "xpos",
        "upos": "upostag",
        "xpos": "xpostag",
    }

    def get(self, key: str, default: T.Optional[T.Any] = None) -> T.Any:
        if key not in self and key in self.MAPPING:
            key = self.MAPPING[key]

        return super(Token, self).get(key, default)

    def __missing__(self, key: str) -> T.Any:
        if key in self.MAPPING:
            return self.get(self.MAPPING[key])

        raise KeyError("'" + key + "'")

    def __str__(self) -> str:
        if 'form' in self:
            return self['form']

        if 'id' in self:
            return f"id={self['id']}"

        return ''

class TokenList(T.List[Token]):
    def __init__(
        self,
        tokens: T.Optional[T.Iterable[Token]] = None,
        metadata: T.Optional[Metadata] = None,
        default_fields: T.Optional[T.Iterable[str]] = None,
    ):
        tokens = tokens or []

        if not isinstance(tokens, list):
            raise ParseException("Can't create TokenList, tokens is not a list.")

        if len(tokens) > 0 and not isinstance(tokens[0], Token):
            tokens = [Token(token) for token in tokens]

        super(TokenList, self).__init__(tokens)

        self.metadata = metadata or Metadata()
        self.default_fields = default_fields

    def __repr__(self) -> str:
        tokens = ', '.join(str(token) for token in self)
        if not self.metadata:
            return f'TokenList<{tokens}>'
        else:
            metadata = ', '.join(f"{key}: \"{value}\"" for key, value in self.metadata.items())
            return f'TokenList<{tokens}, metadata={{{metadata}}}>'

    def __eq__(self, other: T.Any) -> bool:
        if not isinstance(other, TokenList):
            other = TokenList(other)

        return super(TokenList, self).__eq__(other) and self.metadata == other.metadata

    def __ne__(self, other: T.Any) -> bool:
        return not self == other

    def clear(self) -> None:
        super(TokenList, self).clear()
        self.metadata = Metadata()
        self.default_fields = None

    def copy(self) -> 'TokenList':
        tokens_copy = super().copy()
        return TokenList(tokens_copy, self.metadata, self.default_fields)

    def extend(self, iterable: T.Union['TokenList', T.Iterable[Token]]) -> None:
        if not hasattr(self, "metadata"):
            self.metadata = Metadata()
        if not isinstance(iterable, TokenList):
            iterable = TokenList(iterable)
        super(TokenList, self).extend(iterable)
        self.metadata.update(iterable.metadata)

    def _dict_to_token_and_set_defaults(self, token: T.Union[dict, Token]) -> Token:
        if not isinstance(token, Token):
            token = Token(token)

        if self.default_fields:
            for field in self.default_fields:
                if field not in token:
                    token[field] = "_"

        return token

    def append(self, token: T.Union[dict, Token]) -> None:
        token = self._dict_to_token_and_set_defaults(token)
        super(TokenList, self).append(token)

    def insert(self, i: 'SupportsIndex', token: T.Union[dict, Token]) -> None:
        token = self._dict_to_token_and_set_defaults(token)
        super(TokenList, self).insert(i, token)

    @T.overload
    def __setitem__(self, key: 'SupportsIndex', tokens: T.Union[dict, Token]) -> None: ...  # noqa, pragma: no cover

    @T.overload
    def __setitem__(self, key: slice, tokens: T.Union[T.Iterable[T.Union[dict, Token]], 'TokenList']) -> None: ...  # noqa, pragma: no cover

    def __setitem__(self, key, tokens):  # noqa: F811
        if isinstance(key, slice):
            tokens = [self._dict_to_token_and_set_defaults(token) for token in tokens]
            super(TokenList, self).__setitem__(key, tokens)
        else:
            token = tokens
            token = self._dict_to_token_and_set_defaults(token)
            super(TokenList, self).__setitem__(key, token)

    def serialize(self) -> str:
        return serialize(self)

    @staticmethod
    def head_to_token(sentence: 'TokenList') -> T.Dict[int, T.List[Token]]:
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
            # Also filter out those that have no head, just exclude them from the tree.
            if (token.get("head") is None) or token["head"] < 0:
                continue

            head_indexed[token["head"]].append(token)

        if len(head_indexed[0]) == 0:
            raise ParseException("Found no head node, can't build tree")

        return head_indexed

    def to_tree(self) -> 'TokenTree':
        def _create_tree(head_to_token_mapping: T.Dict[int, T.List[Token]], id_: int = 0) -> T.List['TokenTree']:
            return [
                TokenTree(child, _create_tree(head_to_token_mapping, child["id"]))
                for child in head_to_token_mapping[id_]
            ]

        head_indexed = self.head_to_token(self)
        if len(head_indexed[0]) > 1:
            # Introduce fake root node that multiple root nodes can have a single parent
            head_indexed[-1] = [Token(
                [("id", 0), ("form", "_"), ("deprel", "root")]
            )]
            root = _create_tree(head_indexed, -1)[0]
        else:
            root = _create_tree(head_indexed, 0)[0]

        root.set_metadata(self.metadata)
        return root

    def filter(self, **kwargs: T.Any) -> 'TokenList':
        tokens = self.copy()

        for query, value in kwargs.items():
            filtered_tokens = []
            for token in tokens:
                if callable(value) and value(traverse_dict(token, query)) is True:
                    filtered_tokens.append(token)
                else:
                    if traverse_dict(token, query) == value:
                        filtered_tokens.append(token)

            tokens[:] = filtered_tokens

        return tokens


_T = T.TypeVar("_T")
def traverse_dict(obj: T.Mapping[str, _T], query: str) -> T.Optional[_T]:
    """
        Get elements inside a nested dict, based on a dict query. The query is defined by a
        string separated by '__'. traverse_dict(foo, 'a__b__c') is roughly equivalent to foo[a][b][c] but
        will short circuit to return None if something on the query is None.
    """
    query_split = query.split('__')

    cur_obj: T.Optional[T.Union[_T, T.Mapping[str, _T]]] = obj
    for name in query_split:
        assert isinstance(cur_obj, Mapping)  # help mypy
        cur_obj = cur_obj.get(name, None)
        if cur_obj is None:
            return None
    assert not isinstance(cur_obj, Mapping)  # help mypy
    return cur_obj


class TokenTree(object):
    token: Token
    children: T.List['TokenTree']
    metadata: T.Optional[Metadata]

    def __init__(self, token: Token, children: T.List['TokenTree'], metadata: T.Optional[Metadata] = None):
        self.token = token
        self.children = children
        self.metadata = metadata

    def set_metadata(self, metadata: T.Optional[Metadata]) -> None:
        self.metadata = metadata

    def __repr__(self) -> str:
        return 'TokenTree<' + \
            'token={id=' + str(self.token['id']) + ', form=' + str(self.token['form']) + '}, ' + \
            'children=' + ('[...]' if self.children else 'None') + \
            '>'

    def __eq__(self, other: T.Any) -> bool:
        if isinstance(other, TokenTree):
            return self.token == other.token and self.children == other.children \
                and self.metadata == other.metadata
        return False

    def to_list(self):
        def _to_list(root_token: TokenTree, token_list: T.List[Token] = []) -> T.List[Token]:
            token_list.append(root_token.token)

            for child_token in root_token.children:
                _to_list(child_token, token_list)

            return token_list

        if not self.token or "id" not in self.token:
            raise ParseException("Could not flatten tree; missing 'id' field.")

        token_list = _to_list(self)
        token_list = sorted(token_list, key=lambda t: t['id'])
        token_list = TokenList(token_list, self.metadata)

        return token_list

    def serialize(self) -> str:
        return serialize(self.to_list())

    def print_tree(self, depth: int = 0, indent: int = 4,
                   exclude_fields: T.Sequence[str] = DEFAULT_EXCLUDE_FIELDS) -> None:
        if not self.token:
            raise ParseException("Can't print, token is None.")

        if "deprel" not in self.token or "id" not in self.token:
            raise ParseException("Can't print, token is missing either the id or deprel fields.")

        relevant_data = self.token.copy()
        for key in exclude_fields:
            if key in relevant_data:
                del relevant_data[key]

        node_repr = ' '.join([
            '{key}:{value}'.format(key=key, value=value)
            for key, value in relevant_data.items()
        ])

        print(' ' * indent * depth + '(deprel:{deprel}) {node_repr} [{idx}]'.format(
            deprel=self.token['deprel'],
            node_repr=node_repr,
            idx=self.token['id'],
        ))
        for child in self.children:
            child.print_tree(depth=depth + 1, indent=indent, exclude_fields=exclude_fields)

class SentenceList(T.List[TokenList]):
    def __init__(
        self,
        sentences: T.Optional[T.Iterable[TokenList]] = None,
        metadata: T.Optional[Metadata] = None,
    ):
        sentences = sentences or []

        if hasattr(sentences, "__next__"):
            sentences = list(sentences)

        if not isinstance(sentences, list):
            raise ParseException("Can't create SentenceList, sentences is not a list.")

        super(SentenceList, self).__init__(sentences)

        self.metadata = metadata or Metadata()

    def __repr__(self) -> str:
        sentences = ', '.join(str(sentence) for sentence in self)
        if not self.metadata:
            return f'[{sentences}]'
        else:
            metadata = ', '.join(f"{key}: \"{value}\"" for key, value in self.metadata.items())
            return f'SentenceList<{sentences}, metadata={{{metadata}}}>'

    def __eq__(self, other: T.Any) -> bool:
        if not isinstance(other, SentenceList):
            other = SentenceList(other)

        return super(SentenceList, self).__eq__(other) and self.metadata == other.metadata

    def __ne__(self, other: T.Any) -> bool:
        return not self == other

    @T.overload
    def __getitem__(self, key: 'SupportsIndex') -> TokenList: ...  # noqa, pragma: no cover

    @T.overload
    def __getitem__(self, key: slice) -> "SentenceList": ...  # noqa, pragma: no cover

    def __getitem__(self, key):  # noqa: F811
        if isinstance(key, slice):
            return SentenceList(
                sentences=super(SentenceList, self).__getitem__(key),
                metadata=self.metadata
            )
        else:
            return super(SentenceList, self).__getitem__(key)

    def clear(self) -> None:
        super(SentenceList, self).clear()
        self.metadata = Metadata()

    def copy(self) -> 'SentenceList':
        sentences_copy = super().copy()
        return SentenceList(sentences_copy, self.metadata)

    def extend(self, iterable: T.Union['SentenceList', T.Iterable[TokenList]]) -> None:
        if not hasattr(self, "metadata"):
            self.metadata = Metadata()
        if not isinstance(iterable, SentenceList):
            iterable = SentenceList(iterable)

        super(SentenceList, self).extend(iterable)

        self.metadata.update(iterable.metadata)


class SentenceGenerator(T.Iterable[TokenList]):
    def __init__(
        self,
        sentences: T.Iterator[TokenList],
        metadata: T.Optional[Metadata] = None,
    ):
        if isinstance(sentences, T.List):
            sentences = iter(sentences)

        if not isinstance(sentences, T.Iterator):
            raise ParseException("Can't create SentenceGenerator, sentences is not an iterator.")

        self.sentences = sentences
        self.metadata = metadata or Metadata()

    def __iter__(self) -> T.Iterator[TokenList]:
        return self.sentences.__iter__()

    def __next__(self) -> TokenList:
        return self.sentences.__next__()

    def __repr__(self) -> str:
        if not self.metadata:
            return f'SentenceGenerator<{id(self)}>'
        else:
            metadata = ', '.join(f"{key}: \"{value}\"" for key, value in self.metadata.items())
            return f'SentenceGenerator<{id(self)}, metadata={{{metadata}}}>'
