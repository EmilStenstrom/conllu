from __future__ import print_function, unicode_literals

from conllu.compat import text
from conllu.parser import ParseException, head_to_token, serialize

DEFAULT_EXCLUDE_FIELDS = ('id', 'deprel', 'xpostag', 'feats', 'head', 'deps', 'misc')

class TokenList(object):
    tokens = None
    metadata = None

    def __init__(self, tokens, metadata=None):
        if not isinstance(tokens, list):
            raise ParseException("Can't create TokenList, tokens is not a list.")

        self.tokens = tokens
        self.metadata = metadata

    def __getitem__(self, key):
        return self.tokens[key]

    def __repr__(self):
        return 'TokenList<' + ', '.join([token['form'] for token in self.tokens]) + '>'

    def __eq__(self, other):
        return self.tokens == other.tokens and self.metadata == other.metadata

    def serialize(self):
        return serialize(self)

    def to_tree(self):
        def _create_tree(head_to_token_mapping, id_=0):
            return [
                TokenTree(child, _create_tree(head_to_token_mapping, child["id"]))
                for child in head_to_token_mapping[id_]
            ]

        root = _create_tree(head_to_token(self))[0]
        root.set_metadata(self.metadata)
        return root

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
