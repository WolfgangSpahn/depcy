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
    >>> import spacy
    >>> nlp = spacy.load("en_core_web_sm")

    >>> from depcy.utils import tree_view

    >>> doc = nlp("Tom plays tennis and Jo plays socker")  
    >>> print(splitIntoSubtrees(doc))
    Tom plays tennis. Jo plays socker.

    >>> doc1 = nlp("The soldier and the teacher walk home and take supper and drink wine.")
    >>> print(splitIntoSubtrees(doc1))
    The soldier and the teacher walk home. They take supper. They drink wine.

    >>> doc2 = nlp("The soldier and the teacher walk to the pub, which was closed.")
    >>> print(splitIntoSubtrees(doc2))
    The soldier and the teacher walk to the pub. which was closed.

"""

import logging
from pprint import pprint
#
import spacy
from spacy.tokens import Span, Doc, Token
#
from transformers import pipeline
from transformers import logging as hf_logging
#
from depcy.base.string import toStrLeft, toStrRight, toStrSub
from depcy.base.merge import merge_noun_conjs


logger = logging.getLogger(__name__)
hf_logging.set_verbosity_error()

nlp = spacy.load("en_core_web_sm")



def split_sentences(doc):
    """Split sentences on punctuation"""
    logger.debug(f"split_sentences: {doc}")
    start = 0
    for word in doc:
        if word.is_punct and word.text in [".","?","!",";"]:
            yield doc[start:word.i + 1]
            start = word.i + 1

def splitSentConj(doc,depSplit="conj"):
    """
    Split a sentence with a top level conjunction into two sentences.
    """
    logger.debug(f"splitSentConj: {doc}")
    root = next(token for token in doc if token.dep_ == "ROOT")
    root_dict = {token.dep_: token for token in root.children}
    conj = root_dict.get(depSplit,None)
    if conj is None: return doc
    conj_dict = {token.dep_: token for token in conj.children}

    # the first sententce is the original sentence without the conjunction
    textA = f"{toStrLeft(root, avoid=[depSplit])} {root.text} {toStrRight(root, avoid = [depSplit,'cc', 'punct'])}."
    # the second sentence is the conjunction
    # either with its own subject
    csubj = conj_dict.get("nsubj",None)
    if csubj is None:
        textB = f"{root_dict.get('nsubj',None)} {toStrSub(conj, avoid=['punct'])}."
    # or relating to the subject of the first sentence
    else:
        textB = f"{toStrSub(conj, avoid=['punct'])}."
    return nlp(textA.replace(" ,",",") + " " + textB)

def splitUp(doc):
    """
    a simple split up a sentence into pieces
    """
    splits = []
    root = next(doc.sents).root
    for child in root.children:
        if len(list(child.subtree)) > 10:
            childs = list(child.children)
            childs.sort(key=lambda x: x.i)
            for i, grandchild in enumerate(childs):
                if i == 0:
                    gchilds = list(grandchild.subtree)
                    gchilds.append(child)
                    gchilds.sort(key=lambda x: x.i)
                    splits.append(gchilds)
                else:
                    gchilds = list(grandchild.subtree)
                    gchilds.sort(key=lambda x: x.i)
                    splits.append(gchilds)
        else:
            subt = list(child.subtree)
            subt.sort(key=lambda x: x.i)
            splits.append(subt)
    return splits           

def splitSentAtDep(doc,depSplit="ccomp"):
    """
    Split a sentence at a given dependency.
    """
    logger.debug(f"splitSentAtDep: {doc}")

    root = next(token for token in doc if token.dep_ == "ROOT")
    root_subj = next((token for token in root.children if token.dep_ in ["nsubj","nsubjpass"]), None)
    dep = next((token for token in root.children if token.dep_ == depSplit),None)
    if dep is None: return doc
    dep_subj = next((token for token in dep.children if token.dep_ in ["nsubj","nsubjpass"]), None)
    # the first sententce is the original sentence after carvingout the dep subtree
    textA = f"{toStrLeft(root, avoid=[depSplit])} {root.text} {toStrRight(root, avoid = [depSplit,'cc', 'punct'])}."
    # the second sentence is the dep subtree
    # either with its own subject
    if dep_subj: #TODO: check that PRON gender is equals root subject gender
        textB = f"{toStrSub(dep, avoid=['punct'])}."
    # or taking the subject of the first sentence
    else:
        textB = f"_ {toStrSub(dep, avoid=['punct','nsubj','nsubjpass'])}."
    return nlp(textA + " " + textB)

def splitIntoSubtrees(doc, fill_mask=True):
    """ 
        Split a sentence into subtrees headed by a verb. if noFill is False, the <mask> is used instead of the subject.
    """
    doc = merge_noun_conjs(doc) # get conjuncted noun phrases out of the way
    verbs = [token for token in doc if token.pos_ in ["VERB","AUX"] and len(list(token.children)) > 0]

    # Keep track of whether the subject has been printed for each verb
    subject_printed = False

    results = []
    for verb in verbs:
        # Check if the current verb has a subject
        subj = next((token for token in verb.children if token.dep_ in ["nsubj", "nsubjpass"]), None)
        # headSubj = next((token for token in verb.head.children if token.dep_ in ["nsubj", "nsubjpass"]), None)

        # Determine if we need to use the placeholder
        if subj is None and subject_printed:
            subject_prefix = "<mask>"
        else:
            subject_prefix = toStrLeft(verb, avoid=['conj', 'relcl'])
            if subj is not None:
                subject_printed = True  # Update only if the current verb has a subject

        right_str = toStrRight(verb, avoid=['conj','relcl', 'cc', 'punct'])
        result = f"{subject_prefix} {verb.text} {right_str}."
        results.append(result)
      
    if not fill_mask:
        return nlp(" ".join(results))
    else:
        filled = fillPhrases(results)
        return nlp(" ".join(filled))
    
def fillPhrase(context, phrase):
    # Use hugging face llm pipeline to fill the <mask> in the phrase
    # To provide context, we prepend the context with 'and' to the phrase
    classifier = pipeline("fill-mask",model="distilroberta-base",)
    results = classifier(f"{context} and {phrase}")
    if results is not None:
        phrase = results[0]['sequence'].replace(context,"").replace(" and ", "") #type: ignore
    return phrase[0].upper() + phrase[1:]

def fillPhrases(phrases):
    results = []
    for phrase in phrases:
        if '<mask>' in phrase:
            newPharse = fillPhrase(phrases[0],phrase)
        else:
            newPharse = phrase
        results.append(newPharse)
    return results

if __name__ == "__main__":
    import doctest
    doctest.testmod()