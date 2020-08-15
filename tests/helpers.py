from contextlib import redirect_stdout
from io import StringIO


def testlabel(*labels):
    """
    Usage::
        @testlabel('quick')
        class MyTest(unittest.TestCase):
            def test_foo(self):
                pass
    """
    def inner(cls):
        # append labels to class
        cls._labels = set(labels) | getattr(cls, '_labels', set())

        return cls

    return inner

def capture_print(func, args=None):
    f = StringIO()
    with redirect_stdout(f):
        if args:
            func(args)
        else:
            func()

    return f.getvalue()
