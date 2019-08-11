# -*- coding: utf-8 -*-
import os

from setuptools import setup

VERSION = '1.4'

setup(
    name='conllu',
    packages=["conllu"],
    version=VERSION,
    description='CoNLL-U Parser parses a CoNLL-U formatted string into a nested python dictionary',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    author=u'Emil Stenström',
    author_email='em@kth.se',
    url='https://github.com/EmilStenstrom/conllu/',
    install_requires=[],
    keywords=['conllu', 'conll', 'conll-u', 'parser', 'nlp'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
