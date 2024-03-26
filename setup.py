from setuptools import setup, find_packages

setup(
    name='depcy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'spacy',
        'transformers',
        'torch'
    ],
)