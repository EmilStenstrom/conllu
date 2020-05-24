from __future__ import print_function, unicode_literals

from collections import OrderedDict, defaultdict

from conllu.compat import text
from conllu.exceptions import ParseException
from conllu.serializer import serialize

DEFAULT_EXCLUDE_FIELDS = ('id', 'deprel', 'xpos', 'feats', 'head', 'deps', 'misc')

class Metadata(OrderedDict):
    pass

class Token(OrderedDict):
    def __missing__(self, key):
        if key == "upostag":
            return self["upos"]

        if key == "xpostag":
            return self["xpos"]

        if key == "upos":
            return self["upostag"]

        if key == "xpos":
            return self["xpostag"]

        raise KeyError("'" + key + "'")

class TokenList(list):
    metadata = None

    def __init__(self, tokens, metadata=None):
        super(TokenList, self).__init__(tokens)
        if not isinstance(tokens, list):
            raise ParseException("Can't create TokenList, tokens is not a list.")

        self.metadata = metadata

    def __repr__(self):
        return 'TokenList<' + ', '.join(token['form'] for token in self) + '>'

    def __eq__(self, other):
        return super(TokenList, self).__eq__(other) \
            and (not hasattr(other, 'metadata') or self.metadata == other.metadata)

    def __ne__(self, other):
        return not self == other

    def clear(self):
        self[:] = []  # Supported in Python 2 and 3, unlike clear()
        self.metadata = None

    def copy(self):
        tokens_copy = self[:]  # Supported in Python 2 and 3, unlike copy()
        return TokenList(tokens_copy, self.metadata)

    def extend(self, iterable):
        super(TokenList, self).extend(iterable)
        if hasattr(iterable, 'metadata'):
            if hasattr(self.metadata, '__add__') and hasattr(iterable.metadata, '__add__'):
                self.metadata += iterable.metadata
            elif type(self.metadata) is dict and type(iterable.metadata) is dict:
                # noinspection PyUnresolvedReferences
                self.metadata.update(iterable.metadata)
            else:
                self.metadata = [self.metadata, iterable.metadata]

    @property
    def tokens(self):
        return self

    @tokens.setter
    def tokens(self, value):
        self[:] = value  # Supported in Python 2 and 3, unlike clear()

    def serialize(self):
        return serialize(self)

    @staticmethod
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

    def to_tree(self):
        def _create_tree(head_to_token_mapping, id_=0):
            return [
                TokenTree(child, _create_tree(head_to_token_mapping, child["id"]))
                for child in head_to_token_mapping[id_]
            ]

        root = _create_tree(self.head_to_token(self))[0]
        root.set_metadata(self.metadata)
        return root

    def filter(self, **kwargs):
        tokens = self.tokens.copy()

        for query, value in kwargs.items():
            filtered_tokens = []
            for token in tokens:
                if traverse_dict(token, query) == value:
                    filtered_tokens.append(token)

            tokens = filtered_tokens

        return TokenList(tokens)

def traverse_dict(obj, query):
    """
        Get elements inside a nested dict, based on a dict query. The query is defined by a
        string separated by '__'. traverse_dict(foo, 'a__b__c') is roughly equivalent to foo[a][b][c] but
        will short circuit to return None if something on the query is None.
    """
    query = query.split('__')
    for name in query:
        obj = obj.get(name, None)
        if obj is None:
            return None
    return obj


class TokenTree(object):
    token = None
    children = None
    metadata = None

    def __init__(self, token, children, metadata=None):
        self.token = token
        self.children = children
        self.metadata = metadata

    def set_metadata(self, metadata):
        self.metadata = metadata

    def __repr__(self):
        return 'TokenTree<' + \
            'token={id=' + text(self.token['id']) + ', form=' + self.token['form'] + '}, ' + \
            'children=' + ('[...]' if self.children else 'None') + \
            '>'

    def __eq__(self, other):
        return self.token == other.token and self.children == other.children \
            and self.metadata == other.metadata

    def serialize(self):
        if not self.token or "id" not in self.token:
            raise ParseException("Could not serialize tree, missing 'id' field.")

        def flatten_tree(root_token, token_list=[]):
            token_list.append(root_token.token)

            for child_token in root_token.children:
                flatten_tree(child_token, token_list)

            return token_list

        tokens = flatten_tree(self)
        tokens = sorted(tokens, key=lambda t: t['id'])
        tokenlist = TokenList(tokens, self.metadata)

        return serialize(tokenlist)

    def print_tree(self, depth=0, indent=4, exclude_fields=DEFAULT_EXCLUDE_FIELDS):
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
