from __future__ import print_function, unicode_literals

from collections import namedtuple

DEFAULT_EXCLUDE_FIELDS = ["id", "deprel", "xpostag", "feats", "head", "deps", "misc"]

TreeNode = namedtuple('TreeNode', ['data', 'children'])

def create_tree(node_children_mapping, start=0):
    subtree = [
        TreeNode(child, create_tree(node_children_mapping, child["id"]))
        for child in node_children_mapping[start]
    ]
    return subtree

def print_tree(node, **kwargs):
    if isinstance(node, list):
        for tree in node:
            _print_one_tree(tree, **kwargs)
    else:
        _print_one_tree(node, **kwargs)

def _print_one_tree(node, depth=0, indent=4, exclude_fields=DEFAULT_EXCLUDE_FIELDS):
    assert isinstance(node, TreeNode), "node not TreeNode %s" % type(node)

    relevant_data = node.data.copy()
    map(lambda x: relevant_data.pop(x, None), exclude_fields)
    node_repr = " ".join([
        "{key}:{value}".format(key=key, value=value)
        for key, value in relevant_data.items()
    ])

    print(" " * indent * depth + "(deprel:{deprel}) {node_repr} [{idx}]".format(
        deprel=node.data["deprel"],
        node_repr=node_repr,
        idx=node.data["id"],
    ))
    for child in node.children:
        _print_one_tree(child, depth + 1, indent=indent, exclude_fields=exclude_fields)
