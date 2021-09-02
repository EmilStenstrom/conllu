import os

from setuptools import setup  # type: ignore

VERSION = '4.4.1'

setup(
    name='conllu',
    packages=["conllu"],
    python_requires=">=3.6",
    package_data={
        "": ["py.typed"]
    },
    version=VERSION,
    license='MIT License',
    description='CoNLL-U Parser parses a CoNLL-U formatted string into a nested python dictionary',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    author=u'Emil Stenström',
    author_email="emil@emilstenstrom.se",
    url='https://github.com/EmilStenstrom/conllu/',
    keywords=['conllu', 'conll', 'conll-u', 'parser', 'nlp'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
