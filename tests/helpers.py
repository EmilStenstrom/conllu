from contextlib import redirect_stdout
from io import StringIO


def capture_print(func, args=None):
    f = StringIO()
    with redirect_stdout(f):
        if args:
            func(args)
        else:
            func()

    return f.getvalue()
