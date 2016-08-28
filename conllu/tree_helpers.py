from __future__ import print_function, unicode_literals
from collections import namedtuple

TreeNode = namedtuple('TreeNode', ['data', 'children'])

def create_tree(node_children_mapping, start=0):
    subtree = [
        TreeNode(child, create_tree(node_children_mapping, child["id"]))
        for child in node_children_mapping[start]
    ]
    return subtree

def print_tree(node, depth=0):
    assert isinstance(node, TreeNode), "node not TreeNode %s" % type(node)

    print("\t" * depth + "(deprel:{deprel}) form:{form}, tag:{tag} [{idx}]".format(
        deprel=node.data["deprel"],
        form=node.data["form"],
        tag=node.data["upostag"],
        idx=node.data["id"],
    ))
    for child in node.children:
        print_tree(child, depth + 1)
