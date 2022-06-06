# CoNLL-U Parser

**CoNLL-U Parser** parses a [CoNLL-U formatted](http://universaldependencies.org/format.html) string into a nested python dictionary. CoNLL-U is often the output of natural language processing tasks.

## Why should you use conllu?

- It's simple. ~300 lines of code.
- It has no dependencies
- Full typing support so your editor can do autocompletion
- Nice set of tests with CI setup: [![Build](https://github.com/EmilStenstrom/conllu/workflows/Run%20tests%20for%20all%20supported%20python%20versions/badge.svg)](https://github.com/EmilStenstrom/conllu/actions?query=workflow%3A%22Run+tests+for+all+supported+python+versions%22)
- It has 100% test branch coverage (and has undergone [mutation testing](https://github.com/boxed/mutmut/))
- It has [![lots of downloads](http://pepy.tech/badge/conllu)](http://pepy.tech/project/conllu)

## Installation

Note: As of conllu 4.0, Python 3.6 is required to install conllu. See [Notes on updating from 3.0 to 4.0](#notes-on-updating-from-30-to-40)

```bash
pip install conllu
```

Or, if you are using [conda](https://conda.io/docs/):

```bash
conda install -c conda-forge conllu
```

## Notes on updating from 3.0 to 4.0

Conllu version 4.0 drops support for Python 2 and all versions of earlier than Python 3.6. If you need support for older versions of python, you can always pin your install to an old version of conllu. You can install it with `pip install conllu==3.1.1`.

## Notes on updating from 2.0 to 3.0

The Universal dependencies 2.0 release changed two of the field names from xpostag -> xpos and upostag -> upos. Version 3.0 of conllu handles this by aliasing the previous names to the new names. This means you can use xpos/upos or xpostag/upostag, they will both return the same thing. This does change the public API slightly, so I've upped the major version to 3.0, but I've taken care to ensure you most likely DO NOT have to update your code when you update to 3.0.

## Notes on updating from 0.1 to 1.0

I don't like breaking backwards compatibility, but to be able to add new features I felt I had to. This means that updating from 0.1 to 1.0 *might* require code changes. Here's a guide on [how to upgrade to 1.0
](https://github.com/EmilStenstrom/conllu/wiki/Migrating-from-0.1-to-1.0).

## Example usage

At the top level, conllu provides two methods, `parse` and `parse_tree`. The first one parses sentences and returns a flat list. The other returns a nested tree structure. Let's go through them one by one.

## Use parse() to parse into a list of sentences

```python
>>> from conllu import parse
>>> 
>>> data = """
... # text = The quick brown fox jumps over the lazy dog.
... 1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
... 2   quick   quick  ADJ    JJ   Degree=Pos                  4   amod    _   _
... 3   brown   brown  ADJ    JJ   Degree=Pos                  4   amod    _   _
... 4   fox     fox    NOUN   NN   Number=Sing                 5   nsubj   _   _
... 5   jumps   jump   VERB   VBZ  Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin   0   root    _   _
... 6   over    over   ADP    IN   _                           9   case    _   _
... 7   the     the    DET    DT   Definite=Def|PronType=Art   9   det     _   _
... 8   lazy    lazy   ADJ    JJ   Degree=Pos                  9   amod    _   _
... 9   dog     dog    NOUN   NN   Number=Sing                 5   nmod    _   SpaceAfter=No
... 10  .       .      PUNCT  .    _                           5   punct   _   _
...
... """
```

Now you have the data in a variable called `data`. Let's parse it:

```python
>>> sentences = parse(data)
>>> sentences
[TokenList<The, quick, brown, fox, jumps, over, the, lazy, dog, ., metadata={text: "The quick brown fox jumps over the lazy dog."}>]
```

<blockquote>

**Advanced usage**: If you have many sentences (say over a megabyte) to parse at once, you can avoid loading them into memory at once by using `parse_incr()` instead of `parse`. It takes an opened file, and returns a generator instead of the list directly, so you need to either iterate over it, or call list() to get the TokenLists out. Here's how you would use it:

```python
from io import open
from conllu import parse_incr

data_file = open("huge_file.conllu", "r", encoding="utf-8")
for tokenlist in parse_incr(data_file):
    print(tokenlist)
```

For most files, `parse` works fine.
</blockquote>

Since one CoNLL-U file usually contains multiple sentences, `parse()` always returns a list of sentences. Each sentence is represented by a TokenList.

```python
>>> sentence = sentences[0]
>>> sentence
TokenList<The, quick, brown, fox, jumps, over, the, lazy, dog, ., metadata={text: "The quick brown fox jumps over the lazy dog."}>
```

The TokenList supports indexing, so you can get the first token, represented by an ordered dictionary, like this:

```python
>>> token = sentence[0]
>>> token
{'id': 1,
     'form': 'The',
     'lemma': 'the',
     ...}
>>> token["form"]
'The'
```

### New in conllu 2.0: `filter()` a TokenList

```python
>>> sentence = sentences[0]
>>> sentence
TokenList<The, quick, brown, fox, jumps, over, the, lazy, dog, ., metadata={text: "The quick brown fox jumps over the lazy dog."}>
>>> sentence.filter(form="quick")
TokenList<quick>
```

By using `filter(field1__field2=value)` you can filter based on subelements further down in a parsed token.

```python
>>> sentence.filter(feats__Degree="Pos")
TokenList<quick, brown, lazy>
```

Filters can also be chained (meaning you can do `sentence.filter(...).filter(...)`), and filtering on multiple properties at the same time (`sentence.filter(field1=value1, field2=value2)`) means that ALL properties must match.

#### New in conllu 4.3: `filter()` a TokenList by lambda

You can also filter using a lambda function as value. This is useful if you, for instance, would like to filter out only tokens with integer ID:s:

```python
>>> from conllu.models import TokenList, Token
>>> sentence2 = TokenList([
...    Token(id=(1, "-", 2), form="It's"),
...    Token(id=1, form="It"),
...    Token(id=2, form="is"),
... ])
>>> sentence2
TokenList<It's, It, is>
>>> sentence2.filter(id=lambda x: type(x) is int)
TokenList<It, is>
```

### Writing data back to a TokenList

If you want to change your CoNLL-U file, there are a couple of convenience methods to know about.

You can add a new token by simply appending a dictionary with the fields you want to a TokenList:

```python
>>> sentence3 = TokenList([
...    {"id": 1, "form": "Lazy"},
...    {"id": 2, "form": "fox"},
... ])
>>> sentence3
TokenList<Lazy, fox>
>>> sentence3.append({"id": 3, "form": "box"})
>>> sentence3
TokenList<Lazy, fox, box>
```

Changing a sentence just means indexing into it, and setting a value to what you want:

```python
>>> sentence4 = TokenList([
...    {"id": 1, "form": "Lazy"},
...    {"id": 2, "form": "fox"},
... ])
>>> sentence4[1]["form"] = "crocodile"
>>> sentence4
TokenList<Lazy, crocodile>
>>> sentence4[1] = {"id": 2, "form": "elephant"}
>>> sentence4
TokenList<Lazy, elephant>
```

If you omit a field when passing in a dict, conllu will fill in a "_" for those values.

```python
>>> sentences = parse("1  The")
>>> sentences[0].append({"id": 2})
>>> sentences[0]
TokenList<The, _>
```

### Parse metadata from a CoNLL-U file

Each sentence can also have metadata in the form of comments before the sentence starts. This is available in a property on the TokenList called `metadata`.

```python
>>> sentence.metadata
{'text': 'The quick brown fox jumps over the lazy dog.'}
```

### Turn a TokenList back into CoNLL-U

If you ever want to get your CoNLL-U formated text back (maybe after changing something?), use the `serialize()` method:

```python
>>> print(sentence.serialize())
# text = The quick brown fox jumps over the lazy dog.
1   The     the     DET    DT   Definite=Def|PronType=Art   4   det    _   _
2   quick   quick   ADJ    JJ   Degree=Pos                  4   amod   _   _
3   brown   brown   ADJ    JJ   Degree=Pos                  4   amod   _   _
4   fox     fox     NOUN   NN   Number=Sing                 5   nsubj  _   _
5   jumps   jump    VERB   VBZ  Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin   0   root   _   _
6   over    over    ADP    IN   _                           9   case   _   _
7   the     the     DET    DT   Definite=Def|PronType=Art   9   det    _   _
8   lazy    lazy    ADJ    JJ   Degree=Pos                  9   amod   _   _
9   dog     dog     NOUN   NN   Number=Sing                 5   nmod   _   SpaceAfter=No
10  .       .       PUNCT  .    _                           5   punct  _   _
```

### Turn a TokenList into a TokenTree (see below)

You can also convert a TokenList to a TokenTree by using `to_tree`:

```python
>>> sentence.to_tree()
TokenTree<token={id=5, form=jumps}, children=[...]>
```

That's it!

## Use parse_tree() to parse into a list of dependency trees

Sometimes you're interested in the tree structure that hides in the `head` column of a CoNLL-U file. When this is the case, use `parse_tree` to get a nested structure representing the sentence.

```python
>>> from conllu import parse_tree
>>> sentences = parse_tree(data)
>>> sentences
[TokenTree<...>]
```

<blockquote>

**Advanced usage**: If you have many sentences (say over a megabyte) to parse at once, you can avoid loading them into memory at once by using `parse_tree_incr()` instead of `parse_tree`. It takes an opened file, and returns a generator instead of the list directly, so you need to either iterate over it, or call list() to get the TokenTrees out. Here's how you would use it:

```python
from io import open
from conllu import parse_tree_incr

data_file = open("huge_file.conllu", "r", encoding="utf-8")
for tokentree in parse_tree_incr(data_file):
    print(tokentree)
```

</blockquote>

Since one CoNLL-U file usually contains multiple sentences, `parse_tree()` always returns a list of sentences. Each sentence is represented by a TokenTree.

```python
>>> root = sentences[0]
>>> root
TokenTree<token={id=5, form=jumps}, children=[...]>
```

To quickly visualize the tree structure you can call `print_tree` on a TokenTree.

```python
>>> root.print_tree()
(deprel:root) form:jumps lemma:jump upos:VERB [5]
    (deprel:nsubj) form:fox lemma:fox upos:NOUN [4]
        (deprel:det) form:The lemma:the upos:DET [1]
        (deprel:amod) form:quick lemma:quick upos:ADJ [2]
        (deprel:amod) form:brown lemma:brown upos:ADJ [3]
    (deprel:nmod) form:dog lemma:dog upos:NOUN [9]
        (deprel:case) form:over lemma:over upos:ADP [6]
        (deprel:det) form:the lemma:the upos:DET [7]
        (deprel:amod) form:lazy lemma:lazy upos:ADJ [8]
    (deprel:punct) form:. lemma:. upos:PUNCT [10]
```

To access the token corresponding to the current node in the tree, use `token`:

```python
>>> root.token
{
    'id': 5,
    'form': 'jumps',
    'lemma': 'jump',
    ...
}
```

To start walking down the children of the current node, use the children attribute:

```python
>>> children = root.children
>>> children
[
    TokenTree<token={id=4, form=fox}, children=[...]>,
    TokenTree<token={id=9, form=dog}, children=[...]>,
    TokenTree<token={id=10, form=.}, children=None>
]
```

Just like with `parse()`, if a sentence has metadata it is available in a property on the TokenTree root called `metadata`.

```python
>>> root.metadata
{'text': 'The quick brown fox jumps over the lazy dog.'}
```

If you ever want to get your CoNLL-U formated text back (maybe after changing something?), use the `serialize()` method:

```python
>>> print(root.serialize())
# text = The quick brown fox jumps over the lazy dog.
1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
2   quick   quick  ADJ    JJ   Degree=Pos                  4   amod    _   _
...
```

If you want to write it back to a file, you can use something like this:

```python
>>> from conllu import parse_tree
>>> sentences = parse_tree(data)
>>> 
>>> # Make some change to sentences here
>>> 
>>> with open('file-to-write-to', 'w') as f:
...     f.writelines([sentence.serialize() + "\n" for sentence in sentences])
```

## Customizing parsing to handle strange variations of CoNLL-U

Far from all CoNLL-U files found in the wild follow the CoNLL-U format specification. CoNLL-U tries to parse even files that are malformed according to the specification, but sometimes that doesn't work. For those situations you can change how conllu parses your files.

A normal CoNLL-U file consists of a specific set of fields (id, form, lemma, and so on...). Let's walk through how to parse a custom format using the three options `fields`, `field_parsers`, `metadata_parsers`. Here's the custom format we'll use.

```python
>>> data = """
... # tagset = TAG1|TAG2|TAG3|TAG4
... # sentence-123
... 1   My       TAG1|TAG2
... 2   custom   TAG3
... 3   format   TAG4
...
... """
```

Now, let's parse this with the the default settings, and look specifically at the first token to see how it was parsed.

```python
>>> sentences = parse(data)
>>> sentences[0][0]
{'id': 1, 'form': 'My', 'lemma': 'TAG1|TAG2'}
```

The parser has assumed (incorrectly) that the third field must the the default ´lemma´ field and parsed it as such. Let's customize this so the parser gets the name right, by setting the `fields` parameter when calling parse.

```python
>>> sentences = parse(data, fields=["id", "form", "tag"])
>>> sentences[0][0]
{'id': 1, 'form': 'My', 'tag': 'TAG1|TAG2'}
```

The only difference is that you now get the correct field name back when parsing. Now let's say you want those two tags returned as a list instead of as a string. This can be done using the `field_parsers` argument.

```python
>>> split_func = lambda line, i: line[i].split("|")
>>> sentences = parse(data, fields=["id", "form", "tag"], field_parsers={"tag": split_func})
>>> sentences[0][0]
{'id': 1, 'form': 'My', 'tag': ['TAG1', 'TAG2']}
```

That's much better! `field_parsers` specifies a mapping from a field name, to a function that can parse that field. In our case, we specify that the field with custom logic is `"tag"` and that the function to handle it is `split_func`. Each field_parser gets sent two parameters:

* `line`: The whole list of values from this line, split on whitespace. The reason you get the full line is so you can merge several tokens into one using a field_parser if you want.
* `i`: The current location in the line where you currently are. Most often, you'll use `line[i]` to get the current value.

In our case, we return `line[i].split("|")`, which returns a list like we want.

Let's look at the metadata in this example.

```text
# tagset = TAG1|TAG2|TAG3|TAG4
# sentence-123
```

None of these values are valid in CoNLL-U, but since the first line follows the key-value format of other (valid) fields, conllu will parse it anyway:

```python
>>> sentences = parse(data)
>>> sentences[0].metadata
{'tagset': 'TAG1|TAG2|TAG3|TAG4'}
```

Let's return this as a list using the `metadata_parsers` parameter.

```python
>>> sentences = parse(data, metadata_parsers={"tagset": lambda key, value: (key, value.split("|"))})
>>> sentences[0].metadata
{'tagset': ['TAG1', 'TAG2', 'TAG3', 'TAG4']}
```

A metadata parser behaves similarily to a field parser, but since most comments you'll see will be of the form "key = value" these values will be parsed and cleaned first, and then sent to your custom metadata_parser. Here we just take the value, and split it on "|", and return a list back. And lo and behold, we get what we wanted!

Now, let's deal with the "sentence-123" comment. Specifying another metadata_parser won't work, because this is an ID that will be different for each sentence. Instead, let's use a special metadata parser, called `__fallback__`.

```python
>>> sentences = parse(data, metadata_parsers={
...    "tagset": lambda key, value: (key, value.split("|")),
...    "__fallback__": lambda key, value: ("sentence-id", key)
... })
>>> sentences[0].metadata
{
    'tagset': ['TAG1', 'TAG2', 'TAG3', 'TAG4'],
    'sentence-id': 'sentence-123'
}
```

Just what we wanted! `__fallback__` gets called any time none of the other metadata_parsers match, and just like the others, it gets sent the key and value of the current line. In our case, the line contains no "=" to split on, so key will be "sentence-123" and value will be empty. We can return whatever we want here, but let's just say we want to call this field "sentence-id" so we return that as the key, and "sentence-123" as our value.

Finally, consider an even trickier case.

```python
>>> data = """
... # id=1-document_id=36:1047-span=1
... 1   My       TAG1|TAG2
... 2   custom   TAG3
... 3   format   TAG4
...
... """
```

This is actually three different comments, but somehow they are separated by "-" instead of on their own lines. To handle this, we get to use the ability of a metadata_parser to return multiple matches from a single line.

```python
>>> sentences = parse(data, metadata_parsers={
...    "__fallback__": lambda key, value: [pair.split("=") for pair in (key + "=" + value).split("-")]
... })
>>> sentences[0].metadata
{
    'id': '1',
    'document_id': '36:1047',
    'span': '1'
}
```

Our fallback parser returns a **list** of matches, one per pair of metadata comments we find. The `key + "=" + value` trick is needed since by default conllu assumes that this is a valid comment, so `key` is "id" and `value` is everything after the first "=", `1-document_id=36:1047-span=1` (note the missing "id=" in the beginning). We need to add it back before splitting on "-".

And that's it! Using these tricks you should be able to parse all the strange files you stumble into.

## Develop locally and run the tests

1. Make a fork of the repository to your own GitHub account.

2. Clone the repository locally on your computer:
    ```bash
    git clone git@github.com:YOURUSERNAME/conllu.git conllu
    cd conllu
    ```

3. Install the library used for running the tests:
    ```bash
    pip install tox
    ```

4. Now you can run the tests:
    ```bash
    tox
    ```
    This runs tox across all supported versions of Python, and also runs checks for code-coverage, syntax errors, and how imports are sorted.

4. (Alternative) If you just have one version of python installed, and don't want to go through the hassle of installing multiple version of python (hint: Install pyenv and pyenv-tox), **it's fine to run tox with just one version of python**:

    ```bash
    tox -e py36
    ```

5. Make a pull request. Here's a [good guide on PRs from GitHub](https://help.github.com/articles/creating-a-pull-request-from-a-fork/).

Thanks for helping conllu become a better library!
