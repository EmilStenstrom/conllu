try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

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

def capture_print(func, args=None):
    f = StringIO()
    with redirect_stdout(f):
        if args:
            func(args)
        else:
            func()

    return f.getvalue()


try:
    unicode('')
except NameError:
    unicode = str

def text(value):
    return unicode(value)
