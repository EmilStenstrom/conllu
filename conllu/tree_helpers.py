from __future__ import print_function, unicode_literals
from collections import namedtuple

TreeNode = namedtuple('TreeNode', ['data', 'children'])

def create_tree(node_children_mapping, start=0):
    subtree = [
        TreeNode(child, create_tree(node_children_mapping, child["id"]))
        for child in node_children_mapping[start]
    ]
    return subtree

def print_tree(node, depth=0, indent=4, exclude_fields=["id", "deprel", "xpostag", "feats", "head", "deps", "misc"]):
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
        print_tree(child, depth + 1, indent=indent, exclude_fields=exclude_fields)
