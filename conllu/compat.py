from io import StringIO

try:
    from contextlib import redirect_stdout
except ImportError:
    import contextlib
    import sys

    @contextlib.contextmanager
    def redirect_stdout(target):
        original = sys.stdout
        sys.stdout = target
        yield
        sys.stdout = original

def string_to_file(string):
    return StringIO(text(string) if string else None)

def capture_print(func, args=None):
    f = StringIO()
    with redirect_stdout(f):
        if args:
            func(args)
        else:
            func()

    return f.getvalue()


try:
    from re import fullmatch
except ImportError:
    from re import match

    def fullmatch(regex, *args, **kwargs):
        if not regex.pattern.endswith("$"):
            return match(regex.pattern + "$", *args, flags=regex.flags, **kwargs)

        return match(regex.pattern, *args, **kwargs)

try:
    unicode('')
except NameError:
    unicode = str

def text(value):
    return unicode(value)
