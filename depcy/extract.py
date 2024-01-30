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
    Extract tokens from docs or subtrees of docs by part of speech (pos) or dependency (dep).

    We either get a token or a list of tokens.

    Examples:
    >>> from pprint import pprint
    >>> from depcy.utils import tree_view

    >>> nlp = spacy.load("en_core_web_sm")
    >>> text = "The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States, that occurred during the period from around 1760 to about 1820–1840. This transition went from hand production methods to machines, which included new chemical manufacturing, new iron production processes, the increasing use of water power and steam power, the development of machine tools and the rise of the mechanized factory system. Output greatly increased, and the result was an unprecedented rise in population and the rate of population growth. The textile industry was the first to use modern production methods, and textiles became the dominant industry in terms of employment, value of output, and capital invested. Economic historians agree that the onset of the Industrial Revolution is the most important event in human history since the domestication of animals and plants."
    >>> doc = nlp(text)
    >>> sents = list(doc.sents)
    >>> doc1 = sents[0].as_doc()
    >>> docCN = merge_all(doc1, prep=False, compound=True, phrase=False, punct=False, appos=False, conj=False)
    >>> pprint(nouns_propns(docCN))


    >>> tree_view(doc1)
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

    0) we merge all

    >>> doc2 = merge_all(doc1)
    >>> tree_view(doc2)
    +--was|AUX (ROOT|7)
        +--The Industrial Revolution|PROPN (nsubj|0)
        |   +--,|PUNCT (punct|1)
        |   +--known|VERB (acl|3)
        |   |   +--also|ADV (advmod|2)
        |   |   +--as|ADP (prep|4)
        |   |       +--the First Industrial Revolution|PROPN (pobj|5)
        |   +--,|PUNCT (punct|6)
        +--a period of global transition of human economy|NOUN (attr|8)
        |   +--towards|ADP (prep|9)
        |   |   +--more widespread, efficient and stable manufacturing processes|NOUN (pobj|10)
        |   |       +--succeeded|VERB (relcl|12)
        |   |           +--that|PRON (nsubj|11)
        |   |           +--the Agricultural Revolution|PROPN (dobj|13)
        |   +--,|PUNCT (punct|14)
        |   +--starting|VERB (acl|15)
        |       +--from|ADP (prep|16)
        |           +--Great Britain|PROPN (pobj|17)
        |               +--and|CCONJ (cc|18)
        |               +--continental Europe|PROPN (conj|19)
        |                   +--and|CCONJ (cc|20)
        |                   +--the United States|PROPN (conj|21)
        +--,|PUNCT (punct|22)
        +--occurred|VERB (ccomp|24)
        |   +--that|PRON (nsubj|23)
        |   +--during|ADP (prep|25)
        |   |   +--the period|NOUN (pobj|26)
        |   |       +--from|ADP (prep|27)
        |   |           +--around|ADP (prep|28)
        |   |               +--1760|NUM (pobj|29)
        |   +--to|ADP (prep|30)
        |       +--1820–1840|NUM (pobj|32)
        |           +--about|ADP (advmod|31)
        +--.|PUNCT (punct|33)

    1) we get nouns and proper nouns, after the merge

    >>> pprint(nouns_propns(doc2), width=200)
    [The Industrial Revolution,
     the First Industrial Revolution,
     a period of global transition of human economy,
     more widespread, efficient and stable manufacturing processes,
     the Agricultural Revolution,
     Great Britain,
     continental Europe,
     the United States,
     the period]

    2) we get SPOs

    >>> pprint(get_SPOs(doc2), width=200)
    [[a period of global transition of human economy, known, [as, the First Industrial Revolution]],
     [The Industrial Revolution, was, [a period of global transition of human economy, towards, more widespread, efficient and stable manufacturing processes]],
     [that, succeeded, [the Agricultural Revolution]],
     [a period of global transition of human economy, starting, [from, Great Britain, and, continental Europe, and, the United States]],
     [that, occurred, [during, the period, from, around, 1760, to, about, 1820–1840]]]

     3) we get noun phrases

    >>> print(sents[1])
    This transition went from hand production methods to machines, which included new chemical manufacturing, new iron production processes, the increasing use of water power and steam power, the development of machine tools and the rise of the mechanized factory system.
    >>> doc3 = sents[1].as_doc()
    >>> pprint(get_phrases(doc3), width=200)
    [[This transition, went, [from, hand production methods, to, machines]],
     [which,
      included,
      [new chemical manufacturing, new iron production processes, the increasing use of water power, and, steam power, the development of machine tools, and, the rise of the mechanized factory system]]]
    >>> doc3 = merge_all(doc3)


    4) we get phrases

    >>> print(sents[2])
    Output greatly increased, and the result was an unprecedented rise in population and the rate of population growth.
    >>> doc4 = sents[2].as_doc()
    >>> pprint(get_phrases(doc4), width=200)
    [[Output, increased, []], [the result, was, [an unprecedented rise, in, population, and, the rate of population growth]]]


    5) we get phrases

    >>> print(sents[3])
    The textile industry was the first to use modern production methods, and textiles became the dominant industry in terms of employment, value of output, and capital invested.
    >>> doc5 = sents[3].as_doc()
    >>> pprint(get_phrases(doc5), width=200)
    [[The textile industry, was, [the, first]], [first, use, [modern production methods]], [textiles, became, [the dominant industry, in, terms of employment]], [capital, invested, []]]
    >>> pprint([phrasesToStr(p) for p in get_phrases(doc5)], width=200)
    ['The textile industry was the first', 'first use modern production methods', 'textiles became the dominant industry in terms of employment', 'capital invested ']

    6) get phrases from physics text
    >>> text = "Momentum is conserved in this system because there are no external forces acting on it. The system is isolated, and the only forces at play are the internal forces between the two carts during the collision. According to the law of conservation of momentum, the total momentum of an isolated system remains constant. The total momentum before the collision, here just the momentum of cart 1, must equal the total momentum after the collision."
    >>> doc = nlp(text)
    >>> phs = []
    >>> for sent in doc.sents:
    ...     doc_ = sent.as_doc()
    ...     doc_ = merge_verbs(doc_)
    ...     phs.extend(get_phrases_str(doc_))
    >>> pprint(phs, width=200)
    ['Momentum is conserved in this system',
     'there are no external forces',
     'no external forces acting on it',
     'The system is isolated ',
     'the only forces are the internal forces between the two carts during the collision',
     'the total momentum of an isolated system According to the law of conservation of momentum',
     'the total momentum of an isolated system remains constant According to the law of conservation of momentum',
     'The total momentum must equal the total momentum after the collision']

"""
import logging
import spacy
from spacy.tokens import Token, Doc, Span

from depcy.base.navigate import descendants, descendants_and_self
from depcy.base.merge import merge_all, merge_verbs
from depcy.base.string import toStr


logger = logging.getLogger(__name__)

# get specific tokens

def root(tokens):
    """Returns the first root token, in tokens, or None"""
    logger.debug(f"root: {tokens}")
    return next((token for token in tokens if token.dep_ == "ROOT"), None)
def subj(tokens):
    """Returns the first subject of a sentence, or None"""
    logger.debug(f"subj: {tokens}")
    return next((token for token in tokens if token.dep_ in ["nsubj","nsubjpass","expl"]), None)
def obj(tokens):
    """Returns the first  object of a sentence"""
    logger.debug(f"obj: {tokens}")
    return next((token for token in tokens if token.dep_ in ["dobj","attr"]), None)
def attr(tokens):
    """Returns the first attribute of a sentence"""
    logger.debug(f"attr: {tokens}")
    return next((token for token in tokens if token.dep_ == "attr"), None)
def prep(tokens):
    """Returns the preposition of a sentence"""
    logger.debug(f"getPrep: {tokens}")
    return next((token for token in tokens if token.dep_ == "prep"), None)
def aux(tokens):
    """Returns aux"""
    return next((token for token in tokens if token.dep_ == "auxpass"), None)

# get lists of tokens

def preps(tokens):
    """Returns a list of prepositions in a sentence"""
    logger.debug(f"preps: {tokens}")
    return [token for token in tokens if token.dep_ == "prep"]

def verbs(tokens):
    """Returns a list of verbs in a sentence"""
    logger.debug(f"verbs: {tokens}")
    return [token for token in tokens if token.pos_ in ["VERB","AUX"]]

def nouns_propns(tokens):
    """Returns a list of nouns and proper nouns in a sentence"""
    logger.debug(f"nouns_propn: {tokens}")
    return [token for token in tokens if token.pos_ in ["NOUN","PROPN"]]




# get list of tokens and filter by pos or dep

def preps_descendants(token, skip=[]):
    """Returns a list of prepositions and their descendants in a sentence"""
    logger.debug(f"prep_descendants: {token}")
    if token == None: return []
    ps = preps(token.children)
    results = sum([descendants_and_self(p,skip) for p in ps],[])
    results.sort(key=lambda x: x.i)
    return results
def obj_descendants(token, skip=[]):
    """Returns object and its descendants in a sentence"""
    logger.debug(f"obj_descendants: {token}")
    if token == None: return []
    token = obj(token.children)
    if token == None: return []
    results = descendants_and_self(token,skip)

    return results

# get list of lists of tokens and filter by dep

def get_SPOs(tokens):
    """
        Returns a list of subject-predicate-object triples in a sentence.
        TODO: Compare and eventually merge with splitIntoSubtrees
    """
    logger.debug(f"get_SPOs: {tokens}")
    
    spos = []
    for verb_ in verbs(tokens):
        subj_ = subj(verb_.children)
        if subj_ == None: subj_ = verb_subj_ancestors(verb_)[-1]
        preps_ = preps_descendants(verb_,skip=["relcl","acl","appos","punct"])
        obj_ = obj_descendants(verb_,skip=["relcl","acl","appos","punct"])
        spos.append([subj_, verb_,  obj_ + preps_])
    return spos

def get_phrases(doc):
    """Returns a list of phrases in a sentence"""
    assert isinstance(doc, Doc)
    doc = merge_all(doc)
    return get_SPOs(doc)

def get_phrases_str(doc):
    """Returns a list of phrases in a sentence"""
    assert isinstance(doc, Doc)
    doc = merge_all(doc)
    return [phrasesToStr(p) for p in get_SPOs(doc)]

# convert a list of tokens to a string

def phrasesToStr(spo):
    """Returns a string from a spo tuple"""
    s = spo[0].text
    p = spo[1].text
    o = toStr(spo[2])
    return f"{s} {p} {o}"

# get ...

def verb_descendants(tokens, skip=[]):
    """Returns a list of verbs and their descendants in a sentence"""
    logger.debug(f"verb_descendants: {tokens}")
    results = [[token]+descendants(token,skip) for token in tokens if token.pos_ in ["VERB"]]
    for r in results: r.sort(key=lambda x: x.i)
    return results


def ancestors(token):
    """
    Collect the tokens along the path to the root token.
    """
    path_to_root = []
    while token.dep_ != "ROOT":
        path_to_root.append(token)
        token = token.head
    path_to_root.append(token)  # Append the root token
    return path_to_root[::-1]   # Return the reversed list for sentence order

def verb_ancestors(token):
    """Returns ancestors which are verbs"""
    return [a for a in ancestors(token) if a.pos_ in ["VERB","AUX"]]


def verb_subj_ancestors(token):
    """Returns verb-subjects from ancestors"""
    ancs = verb_ancestors(token)
    subjs = []
    for t in ancs:
        subjs.extend([t for t in t.children if t.dep_ in ["nsubj","nsubjpass","attr"]])
    return subjs

if __name__ == "__main__":
    import doctest
    doctest.testmod()