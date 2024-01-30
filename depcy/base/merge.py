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
    This module contains functions to merge tokens in spacy dependency trees.
    Every function takes a spacy doc as input and returns a spacy doc as output.

    In python console use it like this:
    >>> import spacy
    >>> nlp = spacy.load("en_core_web_sm")
    >>> from depcy.base.merge import merge_prepositions, merge_compound_nouns, merge_phrases, merge_punct, merge_appos, merge_all
    >>> from depcy.utils import tree_view

    >>> doc = nlp("The blue, red apple of the apple tree has been fallen.")
    >>> tree_view(doc)
    +--fallen|VERB (ROOT|11)
        +--apple|NOUN (nsubjpass|4)
        |   +--The|DET (det|0)
        |   +--blue|ADJ (amod|1)
        |   +--,|PUNCT (punct|2)
        |   +--red|ADJ (amod|3)
        |   +--of|ADP (prep|5)
        |       +--tree|NOUN (pobj|8)
        |           +--the|DET (det|6)
        |           +--apple|NOUN (compound|7)
        +--has|AUX (aux|9)
        +--been|AUX (auxpass|10)
        +--.|PUNCT (punct|12)

    Now we can merge parts of the tree into single tokens (4).

    1) Merge of prepositions into single tokens.

    >>> tree_view(merge_prepositions(doc))
    +--fallen|VERB (ROOT|7)
        +--apple of the apple tree|NOUN (nsubjpass|4)
        |   +--The|DET (det|0)
        |   +--blue|ADJ (amod|1)
        |   +--,|PUNCT (punct|2)
        |   +--red|ADJ (amod|3)
        +--has|AUX (aux|5)
        +--been|AUX (auxpass|6)
        +--.|PUNCT (punct|8)

    2) Merge of compound nouns into single tokens (7).

    >>> doc = nlp("The blue, red apple of the apple tree has been fallen.")
    >>> tree_view(merge_compound_nouns(doc))
    +--fallen|VERB (ROOT|10)
        +--apple|NOUN (nsubjpass|4)
        |   +--The|DET (det|0)
        |   +--blue|ADJ (amod|1)
        |   +--,|PUNCT (punct|2)
        |   +--red|ADJ (amod|3)
        |   +--of|ADP (prep|5)
        |       +--apple tree|NOUN (pobj|7)
        |           +--the|DET (det|6)
        +--has|AUX (aux|8)
        +--been|AUX (auxpass|9)
        +--.|PUNCT (punct|11)

    3) Merge of noun phrases into single tokens (0,2).

    >>> doc = nlp("The blue, red apple of the apple tree has been fallen.")
    >>> tree_view(merge_phrases(doc))
    +--fallen|VERB (ROOT|5)
        +--The blue, red apple|NOUN (nsubjpass|0)
        |   +--of|ADP (prep|1)
        |       +--the apple tree|NOUN (pobj|2)
        +--has|AUX (aux|3)
        +--been|AUX (auxpass|4)
        +--.|PUNCT (punct|6)

    4) Merge of punctuation into single tokens (10,1).

    >>> doc = nlp("The blue, red apple of the apple tree has been fallen.")
    >>> tree_view(merge_punct(doc))
    +--fallen.|VERB (ROOT|10)
        +--apple|NOUN (nsubjpass|3)
        |   +--The|DET (det|0)
        |   +--blue,|ADJ (amod|1)
        |   +--red|ADJ (amod|2)
        |   +--of|ADP (prep|4)
        |       +--tree|NOUN (pobj|7)
        |           +--the|DET (det|5)
        |           +--apple|NOUN (compound|6)
        +--has|AUX (aux|8)
        +--been|AUX (auxpass|9)

    4) Merge appos into single tokens (8).

    >>> doc = nlp("The blue, red apple of the apple tree, Martas tree, has been fallen.")
    >>> tree_view(merge_appos(doc))
    +--fallen|VERB (ROOT|11)
        +--apple|NOUN (nsubjpass|4)
        |   +--The|DET (det|0)
        |   +--blue|ADJ (amod|1)
        |   +--,|PUNCT (punct|2)
        |   +--red|ADJ (amod|3)
        |   +--of|ADP (prep|5)
        |   +--tree, Martas tree,|NOUN (appos|8)
        |       +--the|DET (det|6)
        |       +--apple|NOUN (compound|7)
        +--has|AUX (aux|9)
        +--been|AUX (auxpass|10)
        +--.|PUNCT (punct|12)

    5) Merge all runs all above merges, except merge_punct.
    >>> doc = nlp("The blue, red apple of the apple tree, Martas tree, has been fallen, Tom and Jerry need to pick it up.")
    >>> doc = merge_all(doc)
    >>> tree_view(doc)
    +--need|VERB (ROOT|8)
        +--fallen|VERB (ccomp|3)
        |   +--The blue, red apple of the apple tree, Martas tree,|NOUN (nsubjpass|0)
        |   +--has|AUX (aux|1)
        |   +--been|AUX (auxpass|2)
        +--,|PUNCT (punct|4)
        +--Tom|PROPN (nsubj|5)
        |   +--and|CCONJ (cc|6)
        |   +--Jerry|PROPN (conj|7)
        +--pick|VERB (xcomp|10)
        |   +--to|PART (aux|9)
        |   +--it|PRON (dobj|11)
        |   +--up|ADP (prt|12)
        +--.|PUNCT (punct|13)
    
    as merga consumes all local comma phrases, we can split the sentence at the remaining comma tokens
    >>> print([ str(part) for part in split_sent_at_commas(doc)])
    ['The blue, red apple of the apple tree, Martas tree, has been fallen', 'Tom and Jerry need to pick it up.']

    >>> doc = nlp("The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States, that occurred during the period from around 1760 to about 1820–1840.")
    >>> doc = merge_all(doc)
    >>> doc = merge_appos(doc, deps = ['acl'])
    >>> tree_view(doc)
    +--was|AUX (ROOT|1)
        +--The Industrial Revolution, also known as the First Industrial Revolution,|PROPN (nsubj|0)
        +--a period of global transition of human economy|NOUN (attr|2)
        |   +--towards|ADP (prep|3)
        |   |   +--more widespread, efficient and stable manufacturing processes|NOUN (pobj|4)
        |   |       +--succeeded|VERB (relcl|6)
        |   |           +--that|PRON (nsubj|5)
        |   +--the Agricultural Revolution, starting|VERB (acl|7)
        |       +--from|ADP (prep|8)
        |           +--Great Britain|PROPN (pobj|9)
        |               +--and|CCONJ (cc|10)
        |               +--continental Europe|PROPN (conj|11)
        |                   +--and|CCONJ (cc|12)
        |                   +--the United States|PROPN (conj|13)
        +--,|PUNCT (punct|14)
        +--occurred|VERB (ccomp|16)
        |   +--that|PRON (nsubj|15)
        |   +--during|ADP (prep|17)
        |   |   +--the period|NOUN (pobj|18)
        |   |       +--from|ADP (prep|19)
        |   |           +--around|ADP (prep|20)
        |   |               +--1760|NUM (pobj|21)
        |   +--to|ADP (prep|22)
        |       +--1820–1840|NUM (pobj|24)
        |           +--about|ADP (advmod|23)
        +--.|PUNCT (punct|25)
    
    >>> print([ str(part) for part in split_sent_at_commas(doc)])
    ['The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States', 'that occurred during the period from around 1760 to about 1820–1840.']

"""
import logging

import spacy
from spacy.matcher import Matcher
from spacy.util import filter_spans
from spacy.tokens import Span, Doc, Token

logger = logging.getLogger(__name__)

nlp = spacy.load("en_core_web_sm")

# You have to set both, Span and Token: TODO: why?
Token.set_extension("is_math", default=False,force=True)
Span.set_extension("is_math", default=False,force=True)
Token.set_extension("math", default="",force=True)
Span.set_extension("math", default="",force=True)

Token.set_extension('ref', default=False, force=True)


def merge_all(doc, prep=True, compound=True, phrase=True, punct=False, appos=True,conj=False):
    """
        Merge prepositions, compound nouns, phrases, and punctuation into single tokens.
    """

    if compound: doc = merge_compound_nouns(doc)
    if phrase: doc = merge_phrases(doc)
    if prep: 
        doc = merge_prepositions(doc)
        doc = merge_prepositions(doc)
    if punct: doc = merge_punct(doc)
    if conj: doc = merge_noun_conjs(doc)
    if appos: doc = merge_appos(doc)
    return doc

def merge_noun_conjs(doc):
    """
        Merge conjunctions into single tokens.
    """
    with doc.retokenize() as retokenizer:
        spans = []
        for token in doc:
            # Check if the token is a conjunction (CC)
            if token.dep_ == 'conj' and token.pos_ in ['PROPN','NOUN']:
                idxs = [token.i]+[c.i for c in token.conjuncts]
                start = min(idxs)
                end = max(idxs)+1
                if start < end:
                        span = doc[start : end]
                        spans.append(span)
                        # Merge the span into a single token
        filtered_spans = filter_spans(spans) # type: ignore
        for span in filtered_spans:
            retokenizer.merge(span)
    return doc

def merge_prepositions(doc):
    """
        Merge prepositions into single tokens.
    """
    with doc.retokenize() as retokenizer:
        spans = []
        for token in doc:
            # Check if the token is a preposition (ADP)
            if token.dep_ == 'prep' and token.text == 'of' and token.head.pos_ in ['NOUN','PROPN']:
                idxs = [token.head.i]+[token.i]+[c.i for c in token.children]
                start = min(idxs)
                end = max(idxs)+1
                if start < end:
                        span = doc[start : end]
                        spans.append(span)
                        # Merge the span into a single token
        filtered_spans = filter_spans(spans)
        for span in filtered_spans:
            retokenizer.merge(span)
    return doc

def merge_appos(doc, deps = ['appos']):
    """
        Merge apostrophe into single tokens.
    """
    with doc.retokenize() as retokenizer:
        spans = []
        for token in doc:
            # Check if the token dep is appos
            if token.dep_ in deps:
                preds = sum([[pred.i for pred in child.subtree if pred.pos_] \
                               for child in token.head.children if child.i < token.i and child.pos_ != "PUNCT"],[])
                succs = [child.i for child in token.head.children if (child.i > token.i and child.pos_ == "PUNCT")]
                sibling = max(preds) if preds else (token.head.i if token.head.pos_ in ["NOUN", "PROPN"] else token.i)
                start = sibling
                end = min(succs)+1 if succs else token.i+1
                if start < end: 
                    span = doc[start : end]
                    spans.append(span)
        filtered_spans = filter_spans(spans)
        for span in filtered_spans:
            retokenizer.merge(span)
    return doc

def merge_verbs(doc):
    with doc.retokenize() as retokenizer:
        spans = []
        for token in doc:
            # Check if the token dep is appos
            if token.pos_ in "VERB":
                adjs = [c for c in token.children if c.pos_ in ["ADJ"]]
                auxs = [c for c in token.children if c.pos_ in ["ADJ", "AUX", "ADV"] if c.i < token.i]
                suppls = adjs + auxs
                idxs = [t.i for t in [token]+suppls]
                if idxs:
                    start = min(idxs)
                    end = max(idxs)+1
                    if start < end:
                        span = doc[start : end]
                        spans.append(span)
        for span in spans:
            retokenizer.merge(span)
    return doc

def merge_compound_nouns(doc):
    """
        Merge compound nouns into single tokens.
    """
    # Create a matcher to find compound nouns
    matcher = Matcher(doc.vocab)
    pattern = [{'DEP': 'compound'}, {'DEP': {'NOT_IN': ['punct', 'compound']}}]
    matcher.add("COMPOUND_NOUN", [pattern])

    # Find matches in the doc
    matches = matcher(doc)

    # Merge compound noun phrases
    spans = []  # To store the spans to merge
    for match_id, start, end in matches:
        span = doc[start:end]  # The matched span
        spans.append(span)

    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)

    return doc

def merge_phrases(doc, avoid = []):
    """
        Merge noun phrases (noun_chunks) into single tokens.
    """
    with doc.retokenize() as retokenizer:
        nps = doc.noun_chunks
        for np in nps:
            attrs = {
                "tag": np.root.tag_,
                "lemma": np.root.lemma_,
                "ent_type": np.root.ent_type_,
            }
            if np[0].pos_ in avoid:
                retokenizer.merge(np[1:], attrs=attrs)
            else:
                retokenizer.merge(np, attrs=attrs)
    return doc


def merge_punct(doc):
    """
        Merge punctuation into single tokens.
    """
    spans = []
    for word in doc[:-1]:
        if word.is_punct or not word.nbor(1).is_punct:
            continue
        start = word.i
        end = word.i + 1
        while end < len(doc) and doc[end].is_punct:
            end += 1
        span = doc[start:end]
        spans.append((span, word.tag_, word.lemma_, word.ent_type_))
    with doc.retokenize() as retokenizer:
        for span, tag, lemma, ent_type in spans:
            attrs = {"tag": tag, "lemma": lemma, "ent_type": ent_type}
            retokenizer.merge(span, attrs=attrs)
    return doc




def merge_date(matcher,doc):
    """Dates are merged into one token"""
    logger.debug(f"merge_date: {doc}")
    matcher.add("DATE", [[ {"ORTH": {"REGEX": r"\d\d"}}, {"ORTH": {"REGEX": r"\d\d"}},
                           {"ORTH": {"REGEX": r"\d\d\d\d"}}]])

    with doc.retokenize() as retokenizer:
        for match_id, start, end in matcher(doc):
            retokenizer.merge(doc[start:end])
    return doc

def merge_math(matcher,doc):
    """Marked math (via'¦') is merged into one token with text and math attributes. 
    After merging, the text is replaced by 'MATH' and the is_math and math (orig tet)
    attributes are set and the text is reparsed"""
    logger.debug(f"merge_math: {doc}")
    start_index = None
    end_index = None
    for i, token in enumerate(doc):
        if token.text == "¦":
            if start_index is None:
                start_index = i
            else:
                end_index = i
                break
    if end_index is None or start_index is None:
        return doc
    # Merge the tokens between the "¦" signs
    # TODO: look for a better alternative to '¦' 
    with doc.retokenize() as retokenizer:
        span = Span(doc, start_index,  end_index+1)
        span._.is_math = True
        retokenizer.merge(span,attrs = {"TAG": "NN","POS": "PROPN","_": {"is_math": True}})
    # a hack: as I could not found a way to change token.text, I am using 
    # the token._.math attribute to store the original text
    math_txts = {i:token.text.strip('¦').strip() for i, token in enumerate(doc) if token._.is_math}
    text = " ".join([token.text if not token._.is_math else "MATH" for token in doc])
    new_doc = nlp(text)
    for i, token in enumerate(new_doc):
        if token.text == "MATH":
            token._.math = math_txts[i]
            token._.is_math = True
    return new_doc

def split_sent_at_commas(doc):
    """Split sentences at commas"""
    logger.debug(f"split_sent_at_commas: {doc}")
    start = 0
    for word in doc:
        if word.text == ",":
            yield doc[start:word.i]
            start = word.i + 1
    yield doc[start:]


if __name__ == "__main__":
    import doctest
    doctest.testmod()