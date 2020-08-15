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
