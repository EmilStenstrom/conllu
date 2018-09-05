from __future__ import unicode_literals

from conllu.models import TokenList
from conllu.parser import parse_token_and_metadata


def parse(data, fields=None):
    return [
        TokenList(*parse_token_and_metadata(sentence, fields=fields))
        for sentence in data.split("\n\n")
        if sentence
    ]

def parse_tree(data):
    tokenlists = parse(data)

    sentences = []
    for tokenlist in tokenlists:
        sentences.append(tokenlist.to_tree())

    return sentences
