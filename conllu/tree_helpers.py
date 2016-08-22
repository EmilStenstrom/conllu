from collections import namedtuple

TreeNode = namedtuple('TreeNode', ['data', 'children'])

def create_tree(node_children_mapping, start=0):
    subtree = [
        TreeNode(child, create_tree(node_children_mapping, child["id"]))
        for child in node_children_mapping[start]
    ]
    return subtree

def print_tree(tree, depth=0):
    for child in tree.children:
        print "\t" * depth + "(deprel:{deprel}) form:{form}, tag:{tag} [{idx}]".format(
            deprel=child.data["deprel"],
            form=child.data["form"],
            tag=child.data["upostag"],
            idx=child.data["id"],
        )
        print_tree(child.children, depth + 1)
