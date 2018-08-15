from __future__ import unicode_literals

from conllu.models import TokenList, TokenTree
from conllu.parser import head_to_token, parse_token_and_metadata


def parse(data, fields=None):
    return [
        TokenList(*parse_token_and_metadata(sentence, fields=fields))
        for sentence in data.split("\n\n")
        if sentence
    ]

def parse_tree(data):
    tokenlists = parse(data)

    def _create_tree(head_to_token_mapping, id_=0):
        return [
            TokenTree(child, _create_tree(head_to_token_mapping, child["id"]))
            for child in head_to_token_mapping[id_]
        ]

    sentences = []
    for tokenlist in tokenlists:
        root = _create_tree(head_to_token(tokenlist))[0]
        root.set_metadata(tokenlist.metadata)
        sentences.append(root)

    return sentences
