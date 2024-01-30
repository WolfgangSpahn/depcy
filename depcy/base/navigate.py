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
    This module contains functions to navigate the spacy dependency trees.
    Every function takes a spacy doc as input and returns a spacy tokens as output.

    In python console use it like this:
    >>> import spacy
    >>> nlp = spacy.load("en_core_web_sm")

    >>> from depcy.utils import tree_view

    >>> doc = nlp("The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States, that occurred during the period from around 1760 to about 1820–1840.")

    Spacy gives us following dependency tree: 
    >>> tree_view(doc)
    +--was|AUX (ROOT|12)
        +--Revolution|PROPN (nsubj|2)
        |   +--The|DET (det|0)
        |   +--Industrial|PROPN (compound|1)
        |   +--,|PUNCT (punct|3)
        |   +--known|VERB (acl|5)
        |   |   +--also|ADV (advmod|4)
        |   |   +--as|ADP (prep|6)
        |   |       +--Revolution|PROPN (pobj|10)
        |   |           +--the|DET (det|7)
        |   |           +--First|PROPN (compound|8)
        |   |           +--Industrial|PROPN (compound|9)
        |   +--,|PUNCT (punct|11)
        +--period|NOUN (attr|14)
        |   +--a|DET (det|13)
        |   +--of|ADP (prep|15)
        |   |   +--transition|NOUN (pobj|17)
        |   |       +--global|ADJ (amod|16)
        |   |       +--of|ADP (prep|18)
        |   |           +--economy|NOUN (pobj|20)
        |   |               +--human|ADJ (amod|19)
        |   +--towards|ADP (prep|21)
        |   |   +--processes|NOUN (pobj|29)
        |   |       +--widespread|ADJ (amod|23)
        |   |       |   +--more|ADV (advmod|22)
        |   |       |   +--,|PUNCT (punct|24)
        |   |       |   +--efficient|ADJ (conj|25)
        |   |       |       +--and|CCONJ (cc|26)
        |   |       |       +--stable|ADJ (conj|27)
        |   |       +--manufacturing|NOUN (compound|28)
        |   |       +--succeeded|VERB (relcl|31)
        |   |           +--that|PRON (nsubj|30)
        |   |           +--Revolution|PROPN (dobj|34)
        |   |               +--the|DET (det|32)
        |   |               +--Agricultural|PROPN (compound|33)
        |   +--,|PUNCT (punct|35)
        |   +--starting|VERB (acl|36)
        |       +--from|ADP (prep|37)
        |           +--Britain|PROPN (pobj|39)
        |               +--Great|PROPN (compound|38)
        |               +--and|CCONJ (cc|40)
        |               +--Europe|PROPN (conj|42)
        |                   +--continental|PROPN (compound|41)
        |                   +--and|CCONJ (cc|43)
        |                   +--States|PROPN (conj|46)
        |                       +--the|DET (det|44)
        |                       +--United|PROPN (compound|45)
        +--,|PUNCT (punct|47)
        +--occurred|VERB (ccomp|49)
        |   +--that|PRON (nsubj|48)
        |   +--during|ADP (prep|50)
        |   |   +--period|NOUN (pobj|52)
        |   |       +--the|DET (det|51)
        |   |       +--from|ADP (prep|53)
        |   |           +--around|ADP (prep|54)
        |   |               +--1760|NUM (pobj|55)
        |   +--to|ADP (prep|56)
        |       +--1820–1840|NUM (pobj|58)
        |           +--about|ADP (advmod|57)
        +--.|PUNCT (punct|59)


    As a simple example, we would like to explore the tokens 'processes' and 'towards.'
    >>> processes = next(token for token in doc if token.text == "processes")
    >>> towards = next(token for token in doc if token.text == "towards")

    Let's get the ancestors of 'processes' (parent, grandparent, etc.):
    >>> print(ancestors(processes))
    [was, period, towards]

    Now the childs
    >>> print(childs(processes))
    [widespread, manufacturing, succeeded]

    And the descendants (children, grandchildren, etc.)
    >>> print(descendants_and_self(processes))
    [more, widespread, ,, efficient, and, stable, manufacturing, processes, that, succeeded, the, Agricultural, Revolution]

    We can also get the right and left descendants (children, grandchildren, etc.) of a token:
    >>> print(right_descendants(processes))
    [that, succeeded, the, Agricultural, Revolution]
    >>> print(left_descendants(processes))
    [more, widespread, ,, efficient, and, stable, manufacturing]

    Or the right and left siblings of a token:
    >>> print(right_siblings(towards))
    [,, starting]
    >>> print(left_siblings(towards))
    [a, of]

    Finally, we can get all tokens that appear before the current token in the document, optionally skipping some branches:
    >>> print(precedings(towards))
    [a, period, of, global, transition, of, human, economy]
    >>> print(root_precedings(towards, skip=['punct','acl']))
    [The, Industrial, Revolution, was, a, period, of, global, transition, of, human, economy]

    Together with merging noun chunks, we can simply resolve 'that' to 'The Industrial Revolution', using rules like this:
    >>> merge_noun_chunks = nlp.add_pipe("merge_noun_chunks")
    >>> doc1 = nlp("The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States, that occurred during the period from around 1760 to about 1820–1840.")
    >>> that = [token for token in doc1 if token.text == "that"]
    >>> print([t for t in root_precedings(that[0], skip=['punct','acl']) if (t.pos_ in ['NOUN','PROPN'] and t.dep_ in ['nsubj'])])
    [The Industrial Revolution]
    >>> print([t for t in root_precedings(that[1], skip=['punct','acl']) if (t.pos_ in ['NOUN','PROPN'] and t.dep_ in ['nsubj'])])
    [The Industrial Revolution]
    
"""

from spacy.tokens.token import Token

def getRoot(token: Token):
    """Returns the root of the current token"""
    if token == None: return None
    while token.dep_ != "ROOT":
        token = token.head
    return token

def walk(token, stop, skip=[]):
    """Walks the dependency tree from the current token, stopping iteration at stop, yielding all tokens"""
    if token == None or token == stop: return
    yield token
    for child in childs(token, skip=skip):
        yield from walk(child, stop, skip=skip)

# ancestors
        
def ancestors(token, skip=[]):
    """Selects all ancestors (parent, grandparent, etc.) of the current token"""
    if token == None: return []
    ancs = []
    while token.dep_ != "ROOT":
        token = token.head
        ancs.append(token)
    return sorted(ancs, key=lambda x: x.i)

def ancestors_and_self(token, skip=[]):
    """Selects all ancestors (parent, grandparent, etc.) of the current token and the token itself"""
    return sorted((ancestors(token, skip=skip) + [token]), key=lambda x: x.i)

# childs

def childs(token, skip=[]):
    """Selects all children of the current token"""
    return [child for child in token.children if child.dep_ not in skip]

# descendants

def descendants(token, skip=[]):
    """Selects all descendants (children, grandchildren, etc.) of the current token"""
    if token == None: return []
    descs = []
    for child in childs(token, skip=skip):
        if child.dep_ not in skip:
            descs.append(child)
            descs.extend(descendants(child, skip=skip))
    return sorted(descs, key=lambda x: x.i)

def descendants_and_self(token, skip=[]):
    """Selects all descendants (children, grandchildren, etc.) of the current token and the token itself"""
    return sorted((descendants(token, skip=skip) + [token]), key=lambda x: x.i)


def right_descendants(token, skip=[]):
    """Selects descendants after (sentence order) the current token in sentence order"""
    return sorted([d for d in descendants(token, skip=skip) if d.i > token.i], key=lambda x: x.i)

def left_descendants(token, skip=[]):
    """Selects descendants before (sentence order) the current token in sentence order"""
    return sorted([d for d in descendants(token, skip=skip) if d.i < token.i], key=lambda x: x.i)

# siblings

def right_siblings(token, skip=[]):
    """Selects all siblings after the current token"""
    siblings = [child for child in token.head.children if child.dep_ not in skip and child.i > token.i]
    return sorted(siblings, key=lambda x: x.i)

def left_siblings(token, skip=[]):
    """Selects all siblings before the current token"""
    siblings = [child for child in token.head.children if child.dep_ not in skip and child.i < token.i]
    return sorted(siblings, key=lambda x: x.i)

# preceding

def precedings(token, skip=[]):
    """Selects all tokens that appear before the current token in the document, originating from its left siblings"""
    result = []
    if token.dep_ == "ROOT": return result
    for sibling in left_siblings(token, skip=skip):
        result.extend(descendants_and_self(sibling, skip=skip))
    return sorted(result+[token.head], key=lambda x: x.i)

def root_precedings(token, skip=[]):
    """Selects all tokens that appear before the current token in the sentence, originating from root"""
    root = getRoot(token)
    result = list(walk(root,token,skip=skip))
    result = [r for r in result if r.i < token.i]
    return sorted(result, key=lambda x: x.i)

if __name__ == "__main__":
    import doctest
    doctest.testmod()