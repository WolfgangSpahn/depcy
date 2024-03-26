from setuptools import setup, find_packages

setup(
    name='depcy',
    version='0.1.0',
    packages=['depcy'],
    install_requires=[
        'spacy',
        'transformers',
        'torch'
    ],
)