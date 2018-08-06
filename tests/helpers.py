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
