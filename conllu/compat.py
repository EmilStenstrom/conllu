try:
    unicode('')
except NameError:
    unicode = str

def text(value):
    return unicode(value)
