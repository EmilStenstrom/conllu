# CoNLL-U Parser

**CoNLL-U Parser** parses a [CoNLL-U formatted](http://universaldependencies.org/format.html) string into a nested python dictionary. CoNLL-U is often the output of natural language processing tasks.

## Why should you use conllu?

- It's simple. ~150 lines of code (including whitespace).
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

## Notes on updating from 0.1 to 0.2

I don't like breaking backwards compatibility, but to be able to add new features I felt I had to. This means that updating from 0.1 to 0.2 *might* require code changes. Here's a guide on [how to upgrade to 0.2](https://github.com/EmilStenstrom/conllu/wiki/Migrating-from-0.1-to-0.2).

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

That's it!

## Use parse_tree() to parse into a list of dependency trees

Sometimes you're interested in the tree structure that hides in the `head` column of a CoNLL-U file. When this is the case, use `parse_tree` to get a nested structure representing the sentence.

```python
>>> from conllu import parse_tree
>>> sentences = parse_tree(data)
>>> sentences
[TokenTree<...>]
```

Since one CoNLL-U file usually contains multiple sentences, `parse_tree()` always returns a list of sentences. Each sentence is represented by a TokenTree.

```python
>>> root = sentences[0]
>>> root
TokenTree<token={id=5, form=jumps, ...}, children=...>
```

The quickly see the tree structure you can call `print` on a TokenTree.

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

```bash
git clone git@github.com:EmilStenstrom/conllu.git
cd conllu
```

Now you can run the tests:

```python
python runtests.py
```

To check that all code really has test, I use a library called coverage. It runs through all code and checks for things that does NOT have tests. This project requires 100% test coverage, and you can easily check if you missed something using this command:

```python
coverage run --source conllu runtests.py; coverage report -m
```

Finally, make sure you follow this project's coding standard by running flake8 on all code.

```python
flake8 conllu tests
```

All these three tests will be run on your finished pull request, and tell you if something went wrong.

Thanks for helping conllu become a better library!
