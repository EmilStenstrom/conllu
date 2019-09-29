import doctest


class Python2DocTestParser(doctest.DocTestParser, object):

    @staticmethod
    def modify_example(example):
        new_want = Python2DocTestParser.add_u_before_strings(example.want)

        example = doctest.Example(
            source=example.source,
            want=new_want,
            exc_msg=example.exc_msg,
            lineno=example.lineno,
            indent=example.indent,
            options=example.options
        )

        return example

    @staticmethod
    def add_u_before_strings(text):
        """Add unicode 'u' in front of strings for Python 2"""
        separator = "'"
        if text.find('"') > text.find("'"):
            separator = '"'

        output = []
        lst = text.split(separator)
        for i, item in enumerate(lst):
            if not i % 2:
                output.append(lst[i])
            else:
                output.append('u' + separator + lst[i] + separator)

        return "".join(output)

    def get_examples(self, *args, **kwargs):
        examples = super(Python2DocTestParser, self).get_examples(*args, **kwargs)
        examples = [Python2DocTestParser.modify_example(example) for example in examples]
        return examples


if object in doctest.DocTestParser.__bases__:
    MyDocTestParser = doctest.DocTestParser
else:
    MyDocTestParser = Python2DocTestParser

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

    def fullmatch(regex, *args):
        if not regex.pattern.endswith("$"):
            return match(regex.pattern + "$", *args)

        return match(regex.pattern, *args)

try:
    unicode('')
except NameError:
    unicode = str

def text(value):
    return unicode(value)
