# coding: utf-8
from __future__ import unicode_literals

import doctest
import os
import re
import shutil
import tempfile

from conllu.compat import MyDocTestParser


class ReadmeTestParser(MyDocTestParser):
    @staticmethod
    def modify_example(example):
        new_source = example.source
        new_want = example.want

        # README is formatted without "..." before multi-line input to make code easy to copy-paste
        if new_source.endswith('"""\n'):
            new_source += new_want + '\n"""'
            new_want = ""

        # doctest sometimes incorrectly includes markdown in returned example
        if new_want.endswith("```\n"):
            new_want = new_want[:new_want.index("```")]

        # README's serialize() has spaces instead of tabs to make output easier to read
        if new_want.startswith("# text"):
            new_want = re.sub(r" {2,}", "\t", new_want)
            new_want = new_want.rstrip() + "\n\n"
            # README cheats and prints return value without quotes
            new_want = repr(new_want)

        # README has examples with lists formatted in multiple lines to make them easier to read
        if new_want.startswith(("[", "OrderedDict([")):
            new_want = ReadmeTestParser.normalize_whitespace(new_want)

        example = doctest.Example(
            source=new_source,
            want=new_want,
            exc_msg=example.exc_msg,
            lineno=example.lineno,
            indent=example.indent,
            options=example.options
        )

        return example

    @staticmethod
    def normalize_whitespace(text):
        """Remove all whitespace except inside strings and after commas"""
        separator = "'"
        if text.find('"') > text.find("'"):
            separator = '"'

        lst = text.split(separator)
        for i, item in enumerate(lst):
            if not i % 2:
                lst[i] = re.sub(r"\s+", "", item)

        text_no_whitespace = separator.join(lst)
        return text_no_whitespace.replace(",", ", ")

    def get_examples(self, *args, **kwargs):
        examples = super(ReadmeTestParser, self).get_examples(*args, **kwargs)
        examples = [ReadmeTestParser.modify_example(example) for example in examples]
        return examples

class ChdirTemp(object):
    def setUp(self, doctest_object):
        self.old_directory = os.getcwd()
        self.tmp_directory = tempfile.mkdtemp()
        os.chdir(self.tmp_directory)

    def tearDown(self, doctest_object):
        os.chdir(self.old_directory)
        shutil.rmtree(self.tmp_directory)

def load_tests(loader, tests, ignore):
    cd = ChdirTemp()
    tests.addTests(
        doctest.DocFileSuite(
            "../README.md",
            parser=ReadmeTestParser(),
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
            setUp=cd.setUp,
            tearDown=cd.tearDown,
        )
    )
    return tests
