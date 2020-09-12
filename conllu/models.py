from __future__ import print_function, unicode_literals

import typing as T
from collections import defaultdict
from collections.abc import Mapping

from conllu.exceptions import ParseException
from conllu.serializer import serialize

DEFAULT_EXCLUDE_FIELDS = ('id', 'deprel', 'xpos', 'feats', 'head', 'deps', 'misc')

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
            return self[self.MAPPING[key]]

        raise KeyError("'" + key + "'")

class TokenList(T.List[Token]):

    metadata: Metadata = Metadata()

    def __init__(self, tokens: T.Iterable[Token], metadata: Metadata = None):
        super(TokenList, self).__init__(tokens)
        if not isinstance(tokens, list):
            raise ParseException("Can't create TokenList, tokens is not a list.")

        self.metadata = metadata or Metadata()

    def __repr__(self) -> str:
        return 'TokenList<' + ', '.join(token['form'] for token in self if 'form' in token) + '>'

    def __eq__(self, other: T.Any) -> bool:
        return super(TokenList, self).__eq__(other) \
            and (not hasattr(other, 'metadata') or self.metadata == other.metadata)

    def __ne__(self, other: T.Any) -> bool:
        return not self == other

    def clear(self) -> None:
        self[:] = []  # Supported in Python 2 and 3, unlike clear()
        self.metadata = Metadata()

    def copy(self) -> 'TokenList':
        tokens_copy = super().copy()
        return TokenList(tokens_copy, self.metadata)

    def extend(self, iterable: T.Union['TokenList', T.Iterable[Token]]) -> None:
        super(TokenList, self).extend(iterable)
        if isinstance(iterable, TokenList):
            self.metadata.update(iterable.metadata)

    @property
    def tokens(self) -> 'TokenList':
        return self

    @tokens.setter
    def tokens(self, value: T.Iterable[Token]) -> None:
        self[:] = value

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
            if token["head"] < 0:
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
        tokens: T.Iterable[Token] = self.tokens.copy()

        for query, value in kwargs.items():
            filtered_tokens = []
            for token in tokens:
                if traverse_dict(token, query) == value:
                    filtered_tokens.append(token)

            tokens = filtered_tokens

        return TokenList(tokens)


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

    def serialize(self) -> str:
        if not self.token or "id" not in self.token:
            raise ParseException("Could not serialize tree, missing 'id' field.")

        def flatten_tree(root_token: TokenTree, token_list: T.List[Token] = []) -> T.List[Token]:
            token_list.append(root_token.token)

            for child_token in root_token.children:
                flatten_tree(child_token, token_list)

            return token_list

        tokens = flatten_tree(self)
        tokens = sorted(tokens, key=lambda t: t['id'])
        tokenlist = TokenList(tokens, self.metadata)

        return serialize(tokenlist)

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
