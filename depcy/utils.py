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
    This module contains functions to split the spacy dependency trees.
    Every function takes a spacy doc as input and returns a spacy doc as output.

    In python console use it like this:
    > import spacy
    > nlp = spacy.load("en_core_web_sm")
    > from depcy.merge import merge_prepositions, merge_compound_nouns, merge_phrases, merge_punct
    > from depcy.transform import tree_view

    > doc = nlp("Tom plays tennis and Jo plays socker")
    > splitSentConj(doc,depSplit="ccomp")
"""

import logging
from transformers import logging as hf_logging
from pprint import pprint
#
import spacy
from spacy.tokens import Span, Doc, Token

from depcy.base.string import toStr

logger = logging.getLogger(__name__)
hf_logging.set_verbosity_error()
nlp = spacy.load("en_core_web_sm")

# --- extensions
# You have to set both, Span and Token: TODO: why?
#
Token.set_extension("depth", default = 0)

# add information to tokens via spacy extensions

def annotate_depth(doc):
    """Annotate the depth of each token in the dependency tree

       !! You need to set the extension depth like this !!

       > Token.set_extension("depth", default = 0)
    """
    logger.debug(f"annotate_depth: {doc}")
    # Assign depth labels to tokens
    def assign_depth(token, depth):
        token._.depth = depth
        for child in token.children:
            assign_depth(child, depth + 1)
    root = next(token for token in doc if token.head == token)
    assign_depth(root, 0)
    return doc



# --- pretty print

def pretty(doc):
    """Petty print a spacy doc"""
    logger.debug(f"pretty: {doc}")
    print(toStr([f"[{t}]" if t.pos_ == "NOUN" else f"({t})" if t.pos_ == "VERB" else f"{t}" for t in doc ]))

def tree_view(doc):
    """
        Print the tree structure of the sentence.
    """
    print_tree(next(token for token in doc if token.dep_ == "ROOT"))

def print_tree(token, indent=0, last=True, prefix=''):
    """Prints a dependency tree starting from a token"""
    line = " " if last else "|"
    print(prefix + "+--" + token.text + "|" + token.pos_ + " (" + token.dep_ +"|"+str(token.i)+ ")")
    prefix += line + "   "
    children = list(token.children)
    for i, child in enumerate(children):
        last = i == (len(children) - 1)
        print_tree(child, indent + 4, last, prefix)

# --- utils

def to_dep_dict(doc):
    """convert a spacy doc to a dictionary"""
    doc_dict = {}
    for tok in doc: 
        if tok.dep_ in doc_dict.keys():
            doc_dict[tok.dep_].append(tok)
        else:
            doc_dict[tok.dep_] = [tok]
    return doc_dict

if __name__ == "__main__":
    import doctest
    doctest.testmod()


