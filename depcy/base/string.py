# Copyright (C) 2023, 2024 Dr. Wolfgang Spahn
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
""" 
    This module converts spacy tokens to strings.

    In python console use it like this:
    >>> import spacy
    >>> nlp = spacy.load("en_core_web_sm")
    >>> from depcy.base.string import toStr, toStrs, toStrSub, toStrLeft, toStrRight
    >>> from depcy.utils import tree_view

    1) concatenate text of tokens to a string in sentence order

    >>> doc = nlp("Tom plays tennis and Jo plays socker")
    >>> print(toStr([t for t in doc]))
    Tom plays tennis and Jo plays socker

    2) concatenate text of subtree of token to a string in sentence order, avoiding tokens with a dependency in avoid

    >>> doc = nlp("The soldier and the teacher from Manchester, walk home and take supper and drink wine.")
    >>> tree_view(doc)
    +--walk|VERB (ROOT|8)
        +--soldier|NOUN (nsubj|1)
        |   +--The|DET (det|0)
        |   +--and|CCONJ (cc|2)
        |   +--teacher|NOUN (conj|4)
        |   |   +--the|DET (det|3)
        |   |   +--from|ADP (prep|5)
        |   |       +--Manchester|PROPN (pobj|6)
        |   +--,|PUNCT (punct|7)
        +--home|ADV (advmod|9)
        +--and|CCONJ (cc|10)
        +--take|VERB (conj|11)
        |   +--supper|NOUN (dobj|12)
        |   +--and|CCONJ (cc|13)
        |   +--drink|VERB (conj|14)
        |       +--wine|NOUN (dobj|15)
        +--.|PUNCT (punct|16)

    >>> take = next(token for token in doc if token.text == "take")
    >>> print(toStrSub(take,avoid=['conj']))
    supper and

    3) concatenate text of left subtree of token to a string in sentence order, avoiding tokens with a dependency in avoid
    >>> teacher = next(token for token in doc if token.text == "teacher")
    >>> print(toStrLeft(teacher,avoid=['conj']))
    the


    4) concatenate text of right subtree of token to a string in sentence order, avoiding tokens with a dependency in avoid
    >>> teacher = next(token for token in doc if token.text == "teacher")
    >>> print(toStrRight(teacher,avoid=['conj']))
    from Manchester


"""
from spacy.tokens import Token

def toStr(tokens: list[Token]):
    """Returns a string from a list of tokens"""
    tokens.sort(key=lambda x: x.i)
    return " ".join([token.text for token in tokens])

def toStrs(list_of_tokens):
    """Returns a list of strings from a list of tokens"""
    strings = []
    for tokens in list_of_tokens:
        tokens.sort(key=lambda x: x.i)
        strings.append(" ".join([token.text for token in tokens]))
    return strings

# convert a subtree to a string representation
def descendants(token, avoid=[]):
    """
    Get all tokens in a subtree of a token, excluding the token itself and tokens with a dependency in avoid.
    """
    if token == None: return []
    descs = []
    for child in token.children:
        if child.dep_ not in avoid:
            descs.append(child)
            descs.extend(descendants(child, avoid))
    return descs

def toStrSub(token, avoid = []):
    """Returns a string representation of a tokens subtree"""   
    if token == None: return ""
    ts = list(descendants(token, avoid)) if token.subtree else []
    ts.sort(key=lambda x: x.i)
    return " ".join([item.text for item in ts])

def toStrLeft(token, avoid = []):
    """Returns a string representation of a tokens left subtree"""
    ts = list(descendants(token, avoid)) if token.subtree else []
    ts.sort(key=lambda x: x.i)
    ts = [t for t in ts if t.i < token.i]
    return " ".join([item.text for item in ts])
def toStrRight(token, avoid = []):
    """Returns a string representation of a tokens right subtree"""
    ts = list(descendants(token, avoid)) if token.subtree else []
    ts.sort(key=lambda x: x.i)
    ts = [t for t in ts if t.i > token.i]
    return " ".join([item.text for item in ts])



if __name__ == "__main__":
    import doctest
    doctest.testmod()