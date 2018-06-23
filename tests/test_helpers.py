import unittest
from contextlib import redirect_stdout

from conllu import print_tree
from conllu.tree_helpers import TreeNode
from io import StringIO


class TestPrintTree(unittest.TestCase):
    def test_print_simple_treenode(self):
        node = TreeNode(data={"id": "X", "deprel": "Y"}, children={})
        result = self._capture_print(print_tree, node)
        self.assertEqual(result, "(deprel:Y) id:X deprel:Y [X]\n")

    def _capture_print(self, func, args):
        f = StringIO()
        with redirect_stdout(f):
            func(args)

        return f.getvalue()
