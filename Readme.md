# Depcy

A simple utility library for navigating and extracting data from spacy dependency trees. You can extract compund nouns, noun phrases and SPO phrases for further use.

When dealing with LLMs there is the need to machine read the language in/ouput. Spacy is a great tool for this. Its dependency tree hold all information you need for this. Depcy helps to keep it simple.

## Docs

https://wolfgangspahn.github.io/depcy_docs.github.io/

## Examples

### Merge all

Merging with merge_all and its sisters is our work horse for simple extraction. 

~~~~ python
from pprint import pprint
from depcy.utils import tree_view

nlp = spacy.load("en_core_web_sm")
text = "The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States, that occurred during the period from around 1760 to about 1820–1840."
doc = nlp(text)
sents = list(doc.sents)
~~~~

By merge_all with default settings we get a deep merge of NOUN related tokens,
~~~~ python
doc1 = sents[0].as_doc()
doc2 = merge_all(doc1)
tree_view(doc2)
~~~~

as you see in the resulting dep tree.

~~~~ bash

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

~~~~

### Extract merged noun phrases

From the merged tree we can now extract the noun phrases with `nouns_prons`

Our dep tree merged with default setting gives a good semantic representation of the key entities, which works well when interacting with LLMs.

~~~ python
pprint(nouns_propns(doc2), width=200)
~~~

a we merged the determiner, noun adjectives, compounds and of-prepositions. 

~~~ bash
[The Industrial Revolution,
the First Industrial Revolution,
a period of global transition of human economy,
more widespread, efficient and stable manufacturing processes,
the Agricultural Revolution,
Great Britain,
continental Europe,
the United States,
the period]
~~~

### Non-default merges

Overwriting the default setting of `merge_all` in all combinations of our sister mergers. Here we effectively just use `merge_compounds`:

~~~~ python
doc0 = sents[0].as_doc()
doc0 = merge_all(doc0, prep=False, compound=True, phrase=False, punct=False, appos=False, conj=False)
pprint(nouns_propns(doc0), width=200)
~~~~

It gives us more the concepts but not the entities.

~~~~ bash
[Industrial Revolution,
First,
Industrial Revolution,
period,
transition,
economy,
manufacturing processes,
Agricultural Revolution,
Great Britain,
continental Europe,
United States,
period]
~~~~ 


### Get key phrases from sentence

``` python
text = "Momentum is conserved in this system because there are no external forces acting on it. The system is isolated, and the only forces at play are the internal forces between the two carts during the collision. According to the law of conservation of momentum, the total momentum of an isolated system remains constant. The total momentum before the collision, here just the momentum of cart 1, must equal the total momentum after the collision."
doc = nlp(text)
phs = []
for sent in doc.sents:
    doc_ = sent.as_doc()
    doc_ = merge_verbs(doc_)
    phs.extend(get_phrases_str(doc_))
pprint(phs, width=200)
```

gives us all major facts in the paragraph in simple sentences, ready for further use.

``` bash
['Momentum is conserved in this system',
    'there are no external forces',
    'no external forces acting on it',
    'The system is isolated ',
    'the only forces are the internal forces between the two carts during the collision',
    'the total momentum of an isolated system According to the law of conservation of momentum',
    'the total momentum of an isolated system remains constant According to the law of conservation of momentum',
    'The total momentum must equal the total momentum after the collision']
```