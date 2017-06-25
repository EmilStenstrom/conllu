# -*- coding: utf-8 -*-
from setuptools import setup

VERSION = '0.4'

setup(
    name='conllu',
    packages=["conllu"],
    version=VERSION,
    description='CoNLL-U Parser parses a CoNLL-U formatted string into a nested python dictionary',
    author=u'Emil Stenström',
    author_email='em@kth.se',
    url='https://github.com/EmilStenstrom/conllu/',
    download_url='https://github.com/EmilStenstrom/conllu/archive/%s.zip' % VERSION,
    install_requires=[],
    tests_require=["nose>=1.3.7", "flake8>=3.0.4"],
    test_suite="nose.collector",
    keywords=['conllu', 'conll', 'conllu-u', 'parser', 'nlp'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
    ],
)
