# CoNLL-U Parser

**CoNLL-U Parser** parses a [CoNLL-U formatted](http://universaldependencies.org/format.html) string into a nested python dictionary. CoNLL-U is often the output of natural language processing tasks.

## Why should you use conllu?

- It's simple. ~300 lines of code.
- Works with both Python 2 and Python 3
- It has no dependencies
- Nice set of tests with CI setup: ![Build status on Travis](https://api.travis-ci.org/EmilStenstrom/conllu.svg?branch=master)
- It has 100% test coverage
- It has [![lots of downloads](http://pepy.tech/badge/conllu)](http://pepy.tech/project/conllu)

## Installation

```bash
pip install conllu
```

Or, if you are using [conda](https://conda.io/docs/):

```bash
conda install -c conda-forge conllu
```

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
# text = The quick brown fox jumps over the lazy dog.
1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
2   quick   quick  ADJ    JJ   Degree=Pos                  4   amod    _   _
3   brown   brown  ADJ    JJ   Degree=Pos                  4   amod    _   _
4   fox     fox    NOUN   NN   Number=Sing                 5   nsubj   _   _
5   jumps   jump   VERB   VBZ  Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin   0   root    _   _
6   over    over   ADP    IN   _                           9   case    _   _
7   the     the    DET    DT   Definite=Def|PronType=Art   9   det     _   _
8   lazy    lazy   ADJ    JJ   Degree=Pos                  9   amod    _   _
9   dog     dog    NOUN   NN   Number=Sing                 5   nmod    _   SpaceAfter=No
10  .       .      PUNCT  .    _                           5   punct   _   _

"""
```

Now you have the data in a variable called `data`. Let's parse it:

```python
>>> sentences = parse(data)
>>> sentences
[TokenList<The, quick, brown, fox, ...>]
```

**Advanced usage**: If you have many sentences (say over a megabyte) to parse at once, you can avoid loading them into memory at once by using `parse_incr()` instead of `parse`. It takes an opened file, and returns a generator instead of the list directly, so you need to either iterate over it, or call list() to get the TokenLists out. Here's how you would use it:

```python
from io import open
from conllu import parse_incr

data_file = open("huge_file.conllu", "r", encoding="utf-8")
for tokenlist in parse_incr(data_file):
    print(tokenlist)
```

For most files, `parse` works fine.

Since one CoNLL-U file usually contains multiple sentences, `parse()` always returns a list of sentences. Each sentence is represented by a TokenList.

```python
>>> sentence = sentences[0]
TokenList<The, quick, brown, fox, ...>
```

The TokenList supports indexing, so you can get the first token, represented by an ordered dictionary, like this:

```
>>> token = sentence[0]
>>> token
OrderedDict([
    ('id', 1),
    ('form', 'The'),
    ('lemma', 'the'),
    ...
])
>>> token["form"]
'The'
```

Each sentence can also have metadata in the form of comments before the sentence starts. This is available in a property on the TokenList called `metadata`.

```python
>>> sentence.metadata
OrderedDict([
    ("text", "The quick brown fox jumps over the lazy dog."),
    ...
])
```

If you ever want to get your CoNLL-U formated text back (maybe after changing something?), use the `serialize()` method:

```python
>>> sentence.serialize()
# text = The quick brown fox jumps over the lazy dog.
1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
2   quick   quick  ADJ    JJ   Degree=Pos                  4   amod    _   _
...
```

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

**Advanced usage**: If you have many sentences (say over a megabyte) to parse at once, you can avoid loading them into memory at once by using `parse_tree_incr()` instead of `parse_tree`. It takes an opened file, and returns a generator instead of the list directly, so you need to either iterate over it, or call list() to get the TokenTrees out. Here's how you would use it:

```python
from io import open
from conllu import parse_tree_incr

data_file = open("huge_file.conllu", "r", encoding="utf-8")
for tokentree in parse_tree_incr(data_file):
    print(tokentree)
```

Since one CoNLL-U file usually contains multiple sentences, `parse_tree()` always returns a list of sentences. Each sentence is represented by a TokenTree.

```python
>>> root = sentences[0]
>>> root
TokenTree<token={id=5, form=jumps, ...}, children=...>
```

To quickly visualize the tree structure you can call `print_tree` on a TokenTree.

```python
>>> root.print_tree()
(deprel:root) form:jumps lemma:jump upostag:VERB [5]
    (deprel:nsubj) form:fox lemma:fox upostag:NOUN [4]
        (deprel:det) form:The lemma:the upostag:DET [1]
        (deprel:amod) form:quick lemma:quick upostag:ADJ [2]
        (deprel:amod) form:brown lemma:brown upostag:ADJ [3]
    (deprel:nmod) form:dog lemma:dog upostag:NOUN [9]
        (deprel:case) form:over lemma:over upostag:ADP [6]
        (deprel:det) form:the lemma:the upostag:DET [7]
        (deprel:amod) form:lazy lemma:lazy upostag:ADJ [8]
    (deprel:punct) form:. lemma:. upostag:PUNCT [10]
```

To access the token corresponding to the current node in the tree, use `token`:

```python
>>> root.token
OrderedDict([
    ('id', 5),
    ('form', 'jumps'),
    ('lemma', 'jump'),
    ...
])
```

To start walking down the children of the current node, use the children attribute:

```python
>>> children = root.children
>>> children
[
    TokenTree<token={id=4, form=fox, ...}, children=...>,
    TokenTree<token={id=9, form=dog, ...}, children=...>,
    TokenTree<token={id=10, form=., ...}, children=...>,
]
```

Just like with `parse()`, if a sentence has metadata it is available in a property on the TokenTree root called `metadata`.

```python
>>> root.metadata
OrderedDict([
    ("text", "The quick brown fox jumps over the lazy dog."),
    ...
])
```

If you ever want to get your CoNLL-U formated text back (maybe after changing something?), use the `serialize()` method:

```python
>>> root.serialize()
# text = The quick brown fox jumps over the lazy dog.
1   The     the    DET    DT   Definite=Def|PronType=Art   4   det     _   _
2   quick   quick  ADJ    JJ   Degree=Pos                  4   amod    _   _
...
```

You can read about the CoNLL-U format at the [Universial Dependencies project](http://universaldependencies.org/format.html).

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
