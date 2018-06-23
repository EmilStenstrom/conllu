import unittest

from conllu import print_tree
from conllu.tree_helpers import TreeNode
from io import StringIO

try:
    from contextlib import redirect_stdout
except ImportError:
    import sys
    import contextlib

    @contextlib.contextmanager
    def redirect_stdout(target):
        original = sys.stdout
        sys.stdout = target
        yield
        sys.stdout = original

class TestPrintTree(unittest.TestCase):
    def test_print_empty_list(self):
        result = self._capture_print(print_tree, [])
        self.assertEqual(result, "")

    def test_print_simple_treenode(self):
        node = TreeNode(data={"id": "X", "deprel": "Y", "test": "data"}, children={})
        result = self._capture_print(print_tree, node)
        self.assertEqual(result, "(deprel:Y) test:data [X]\n")

    def test_print_list_of_nodes(self):
        node = TreeNode(data={"id": "X", "deprel": "Y", "test": "data"}, children={})
        nodes = [node, node]
        result = self._capture_print(print_tree, nodes)
        self.assertEqual(result, "(deprel:Y) test:data [X]\n" * 2)

    def _capture_print(self, func, args):
        f = StringIO()
        with redirect_stdout(f):
            func(args)

        return f.getvalue()
