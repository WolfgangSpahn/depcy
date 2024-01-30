---
description: |
    API documentation for modules: depcy, depcy.base, depcy.base.dep_tags, depcy.base.merge, depcy.base.navigate, depcy.base.string, depcy.extract, depcy.split, depcy.utils.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Namespace `depcy` {#id}




    
## Sub-modules

* [depcy.base](#depcy.base)
* [depcy.extract](#depcy.extract)
* [depcy.split](#depcy.split)
* [depcy.utils](#depcy.utils)






    
# Namespace `depcy.base` {#id}




    
## Sub-modules

* [depcy.base.dep_tags](#depcy.base.dep_tags)
* [depcy.base.merge](#depcy.base.merge)
* [depcy.base.navigate](#depcy.base.navigate)
* [depcy.base.string](#depcy.base.string)






    
# Module `depcy.base.dep_tags` {#id}

This file contains a dictionary of dependency tags, their descriptions, examples and prolog categories.







    
# Module `depcy.base.merge` {#id}

This module contains functions to merge tokens in spacy dependency trees.
Every function takes a spacy doc as input and returns a spacy doc as output.

In python console use it like this:
```python-repl
>>> import spacy
>>> nlp = spacy.load("en_core_web_sm")
>>> from depcy.base.merge import merge_prepositions, merge_compound_nouns, merge_phrases, merge_punct, merge_appos, merge_all
>>> from depcy.utils import tree_view
```


```python-repl
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
```


Now we can merge parts of the tree into single tokens (4).

1) Merge of prepositions into single tokens.

```python-repl
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
```


2) Merge of compound nouns into single tokens (7).

```python-repl
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
```


3) Merge of noun phrases into single tokens (0,2).

```python-repl
>>> doc = nlp("The blue, red apple of the apple tree has been fallen.")
>>> tree_view(merge_phrases(doc))
+--fallen|VERB (ROOT|5)
    +--The blue, red apple|NOUN (nsubjpass|0)
    |   +--of|ADP (prep|1)
    |       +--the apple tree|NOUN (pobj|2)
    +--has|AUX (aux|3)
    +--been|AUX (auxpass|4)
    +--.|PUNCT (punct|6)
```


4) Merge of punctuation into single tokens (10,1).

```python-repl
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
```


4) Merge appos into single tokens (8).

```python-repl
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
```


5) Merge all runs all above merges, except merge_punct.
```python-repl
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
```


as merga consumes all local comma phrases, we can split the sentence at the remaining comma tokens
```python-repl
>>> print([ str(part) for part in split_sent_at_commas(doc)])
['The blue, red apple of the apple tree, Martas tree, has been fallen', 'Tom and Jerry need to pick it up.']
```


```python-repl
>>> doc = nlp("The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States, that occurred during the period from around 1760 to about 1820ΓÇô1840.")
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
    |       +--1820ΓÇô1840|NUM (pobj|24)
    |           +--about|ADP (advmod|23)
    +--.|PUNCT (punct|25)
```


```python-repl
>>> print([ str(part) for part in split_sent_at_commas(doc)])
['The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States', 'that occurred during the period from around 1760 to about 1820ΓÇô1840.']
```





    
## Functions


    
### Function `merge_all` {#id}




>     def merge_all(
>         doc,
>         prep=True,
>         compound=True,
>         phrase=True,
>         punct=False,
>         appos=True,
>         conj=False
>     )


Merge prepositions, compound nouns, phrases, and punctuation into single tokens.

    
### Function `merge_appos` {#id}




>     def merge_appos(
>         doc,
>         deps=['appos']
>     )


Merge apostrophe into single tokens.

    
### Function `merge_compound_nouns` {#id}




>     def merge_compound_nouns(
>         doc
>     )


Merge compound nouns into single tokens.

    
### Function `merge_date` {#id}




>     def merge_date(
>         matcher,
>         doc
>     )


Dates are merged into one token

    
### Function `merge_math` {#id}




>     def merge_math(
>         matcher,
>         doc
>     )


Marked math (via'┬ª') is merged into one token with text and math attributes. 
After merging, the text is replaced by 'MATH' and the is_math and math (orig tet)
attributes are set and the text is reparsed

    
### Function `merge_noun_conjs` {#id}




>     def merge_noun_conjs(
>         doc
>     )


Merge conjunctions into single tokens.

    
### Function `merge_phrases` {#id}




>     def merge_phrases(
>         doc,
>         avoid=[]
>     )


Merge noun phrases (noun_chunks) into single tokens.

    
### Function `merge_prepositions` {#id}




>     def merge_prepositions(
>         doc
>     )


Merge prepositions into single tokens.

    
### Function `merge_punct` {#id}




>     def merge_punct(
>         doc
>     )


Merge punctuation into single tokens.

    
### Function `merge_verbs` {#id}




>     def merge_verbs(
>         doc
>     )




    
### Function `split_sent_at_commas` {#id}




>     def split_sent_at_commas(
>         doc
>     )


Split sentences at commas




    
# Module `depcy.base.navigate` {#id}

This module contains functions to navigate the spacy dependency trees.
Every function takes a spacy doc as input and returns a spacy tokens as output.

In python console use it like this:
```python-repl
>>> import spacy
>>> nlp = spacy.load("en_core_web_sm")
```


```python-repl
>>> from depcy.utils import tree_view
```


```python-repl
>>> doc = nlp("The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States, that occurred during the period from around 1760 to about 1820ΓÇô1840.")
```


Spacy gives us following dependency tree: 
```python-repl
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
    |       +--1820ΓÇô1840|NUM (pobj|58)
    |           +--about|ADP (advmod|57)
    +--.|PUNCT (punct|59)
```



As a simple example, we would like to explore the tokens 'processes' and 'towards.'
```python-repl
>>> processes = next(token for token in doc if token.text == "processes")
>>> towards = next(token for token in doc if token.text == "towards")
```


Let's get the ancestors of 'processes' (parent, grandparent, etc.):
```python-repl
>>> print(ancestors(processes))
[was, period, towards]
```


Now the childs
```python-repl
>>> print(childs(processes))
[widespread, manufacturing, succeeded]
```


And the descendants (children, grandchildren, etc.)
```python-repl
>>> print(descendants_and_self(processes))
[more, widespread, ,, efficient, and, stable, manufacturing, processes, that, succeeded, the, Agricultural, Revolution]
```


We can also get the right and left descendants (children, grandchildren, etc.) of a token:
```python-repl
>>> print(right_descendants(processes))
[that, succeeded, the, Agricultural, Revolution]
>>> print(left_descendants(processes))
[more, widespread, ,, efficient, and, stable, manufacturing]
```


Or the right and left siblings of a token:
```python-repl
>>> print(right_siblings(towards))
[,, starting]
>>> print(left_siblings(towards))
[a, of]
```


Finally, we can get all tokens that appear before the current token in the document, optionally skipping some branches:
```python-repl
>>> print(precedings(towards))
[a, period, of, global, transition, of, human, economy]
>>> print(root_precedings(towards, skip=['punct','acl']))
[The, Industrial, Revolution, was, a, period, of, global, transition, of, human, economy]
```


Together with merging noun chunks, we can simply resolve 'that' to 'The Industrial Revolution', using rules like this:
```python-repl
>>> merge_noun_chunks = nlp.add_pipe("merge_noun_chunks")
>>> doc1 = nlp("The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States, that occurred during the period from around 1760 to about 1820ΓÇô1840.")
>>> that = [token for token in doc1 if token.text == "that"]
>>> print([t for t in root_precedings(that[0], skip=['punct','acl']) if (t.pos_ in ['NOUN','PROPN'] and t.dep_ in ['nsubj'])])
[The Industrial Revolution]
>>> print([t for t in root_precedings(that[1], skip=['punct','acl']) if (t.pos_ in ['NOUN','PROPN'] and t.dep_ in ['nsubj'])])
[The Industrial Revolution]
```





    
## Functions


    
### Function `ancestors` {#id}




>     def ancestors(
>         token,
>         skip=[]
>     )


Selects all ancestors (parent, grandparent, etc.) of the current token

    
### Function `ancestors_and_self` {#id}




>     def ancestors_and_self(
>         token,
>         skip=[]
>     )


Selects all ancestors (parent, grandparent, etc.) of the current token and the token itself

    
### Function `childs` {#id}




>     def childs(
>         token,
>         skip=[]
>     )


Selects all children of the current token

    
### Function `descendants` {#id}




>     def descendants(
>         token,
>         skip=[]
>     )


Selects all descendants (children, grandchildren, etc.) of the current token

    
### Function `descendants_and_self` {#id}




>     def descendants_and_self(
>         token,
>         skip=[]
>     )


Selects all descendants (children, grandchildren, etc.) of the current token and the token itself

    
### Function `getRoot` {#id}




>     def getRoot(
>         token:┬áspacy.tokens.token.Token
>     )


Returns the root of the current token

    
### Function `left_descendants` {#id}




>     def left_descendants(
>         token,
>         skip=[]
>     )


Selects descendants before (sentence order) the current token in sentence order

    
### Function `left_siblings` {#id}




>     def left_siblings(
>         token,
>         skip=[]
>     )


Selects all siblings before the current token

    
### Function `precedings` {#id}




>     def precedings(
>         token,
>         skip=[]
>     )


Selects all tokens that appear before the current token in the document, originating from its left siblings

    
### Function `right_descendants` {#id}




>     def right_descendants(
>         token,
>         skip=[]
>     )


Selects descendants after (sentence order) the current token in sentence order

    
### Function `right_siblings` {#id}




>     def right_siblings(
>         token,
>         skip=[]
>     )


Selects all siblings after the current token

    
### Function `root_precedings` {#id}




>     def root_precedings(
>         token,
>         skip=[]
>     )


Selects all tokens that appear before the current token in the sentence, originating from root

    
### Function `walk` {#id}




>     def walk(
>         token,
>         stop,
>         skip=[]
>     )


Walks the dependency tree from the current token, stopping iteration at stop, yielding all tokens




    
# Module `depcy.base.string` {#id}

This module converts spacy tokens to strings.

In python console use it like this:
```python-repl
>>> import spacy
>>> nlp = spacy.load("en_core_web_sm")
>>> from depcy.base.string import toStr, toStrs, toStrSub, toStrLeft, toStrRight
>>> from depcy.utils import tree_view
```


1) concatenate text of tokens to a string in sentence order

```python-repl
>>> doc = nlp("Tom plays tennis and Jo plays socker")
>>> print(toStr([t for t in doc]))
Tom plays tennis and Jo plays socker
```


2) concatenate text of subtree of token to a string in sentence order, avoiding tokens with a dependency in avoid

```python-repl
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
```


```python-repl
>>> take = next(token for token in doc if token.text == "take")
>>> print(toStrSub(take,avoid=['conj']))
supper and
```


3) concatenate text of left subtree of token to a string in sentence order, avoiding tokens with a dependency in avoid
```python-repl
>>> teacher = next(token for token in doc if token.text == "teacher")
>>> print(toStrLeft(teacher,avoid=['conj']))
the
```



4) concatenate text of right subtree of token to a string in sentence order, avoiding tokens with a dependency in avoid
```python-repl
>>> teacher = next(token for token in doc if token.text == "teacher")
>>> print(toStrRight(teacher,avoid=['conj']))
from Manchester
```





    
## Functions


    
### Function `descendants` {#id}




>     def descendants(
>         token,
>         avoid=[]
>     )


Get all tokens in a subtree of a token, excluding the token itself and tokens with a dependency in avoid.

    
### Function `toStr` {#id}




>     def toStr(
>         tokens:┬álist[spacy.tokens.token.Token]
>     )


Returns a string from a list of tokens

    
### Function `toStrLeft` {#id}




>     def toStrLeft(
>         token,
>         avoid=[]
>     )


Returns a string representation of a tokens left subtree

    
### Function `toStrRight` {#id}




>     def toStrRight(
>         token,
>         avoid=[]
>     )


Returns a string representation of a tokens right subtree

    
### Function `toStrSub` {#id}




>     def toStrSub(
>         token,
>         avoid=[]
>     )


Returns a string representation of a tokens subtree

    
### Function `toStrs` {#id}




>     def toStrs(
>         list_of_tokens
>     )


Returns a list of strings from a list of tokens




    
# Module `depcy.extract` {#id}

Extract tokens from docs or subtrees of docs by part of speech (pos) or dependency (dep).

We either get a token or a list of tokens.

Examples:
```python-repl
>>> from pprint import pprint
>>> from depcy.utils import tree_view
```


```python-repl
>>> nlp = spacy.load("en_core_web_sm")
>>> text = "The Industrial Revolution, also known as the First Industrial Revolution, was a period of global transition of human economy towards more widespread, efficient and stable manufacturing processes that succeeded the Agricultural Revolution, starting from Great Britain and continental Europe and the United States, that occurred during the period from around 1760 to about 1820ΓÇô1840. This transition went from hand production methods to machines, which included new chemical manufacturing, new iron production processes, the increasing use of water power and steam power, the development of machine tools and the rise of the mechanized factory system. Output greatly increased, and the result was an unprecedented rise in population and the rate of population growth. The textile industry was the first to use modern production methods, and textiles became the dominant industry in terms of employment, value of output, and capital invested. Economic historians agree that the onset of the Industrial Revolution is the most important event in human history since the domestication of animals and plants."
>>> doc = nlp(text)
>>> sents = list(doc.sents)
>>> doc1 = sents[0].as_doc()
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
    |       +--1820ΓÇô1840|NUM (pobj|58)
    |           +--about|ADP (advmod|57)
    +--.|PUNCT (punct|59)
```


1) we merge all

```python-repl
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
    |       +--1820ΓÇô1840|NUM (pobj|32)
    |           +--about|ADP (advmod|31)
    +--.|PUNCT (punct|33)
```


2) we get SPOs

```python-repl
>>> pprint(get_SPOs(doc2), width=200)
[[a period of global transition of human economy, known, [as, the First Industrial Revolution]],
 [The Industrial Revolution, was, [a period of global transition of human economy, towards, more widespread, efficient and stable manufacturing processes]],
 [that, succeeded, [the Agricultural Revolution]],
 [a period of global transition of human economy, starting, [from, Great Britain, and, continental Europe, and, the United States]],
 [that, occurred, [during, the period, from, around, 1760, to, about, 1820ΓÇô1840]]]
```


 3) we get noun phrases

```python-repl
>>> print(sents[1])
This transition went from hand production methods to machines, which included new chemical manufacturing, new iron production processes, the increasing use of water power and steam power, the development of machine tools and the rise of the mechanized factory system.
>>> doc3 = sents[1].as_doc()
>>> pprint(get_phrases(doc3), width=200)
[[This transition, went, [from, hand production methods, to, machines]],
 [which,
  included,
  [new chemical manufacturing, new iron production processes, the increasing use of water power, and, steam power, the development of machine tools, and, the rise of the mechanized factory system]]]
>>> doc3 = merge_all(doc3)
```



4) we get phrases

```python-repl
>>> print(sents[2])
Output greatly increased, and the result was an unprecedented rise in population and the rate of population growth.
>>> doc4 = sents[2].as_doc()
>>> pprint(get_phrases(doc4), width=200)
[[Output, increased, []], [the result, was, [an unprecedented rise, in, population, and, the rate of population growth]]]
```



5) we get phrases

```python-repl
>>> print(sents[3])
The textile industry was the first to use modern production methods, and textiles became the dominant industry in terms of employment, value of output, and capital invested.
>>> doc5 = sents[3].as_doc()
>>> pprint(get_phrases(doc5), width=200)
[[The textile industry, was, [the, first]], [first, use, [modern production methods]], [textiles, became, [the dominant industry, in, terms of employment]], [capital, invested, []]]
>>> pprint([phrasesToStr(p) for p in get_phrases(doc5)], width=200)
['The textile industry was the first', 'first use modern production methods', 'textiles became the dominant industry in terms of employment', 'capital invested ']
```


6) get phrases from physics text
```python-repl
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
```





    
## Functions


    
### Function `ancestors` {#id}




>     def ancestors(
>         token
>     )


Collect the tokens along the path to the root token.

    
### Function `attr` {#id}




>     def attr(
>         tokens
>     )


Returns the first attribute of a sentence

    
### Function `aux` {#id}




>     def aux(
>         tokens
>     )


Returns aux

    
### Function `get_SPOs` {#id}




>     def get_SPOs(
>         tokens
>     )


Returns a list of subject-predicate-object triples in a sentence.
TODO: Compare and eventually merge with splitIntoSubtrees

    
### Function `get_phrases` {#id}




>     def get_phrases(
>         doc
>     )


Returns a list of phrases in a sentence

    
### Function `get_phrases_str` {#id}




>     def get_phrases_str(
>         doc
>     )


Returns a list of phrases in a sentence

    
### Function `nouns_propns` {#id}




>     def nouns_propns(
>         tokens
>     )


Returns a list of nouns and proper nouns in a sentence

    
### Function `obj` {#id}




>     def obj(
>         tokens
>     )


Returns the first  object of a sentence

    
### Function `obj_descendants` {#id}




>     def obj_descendants(
>         token,
>         skip=[]
>     )


Returns object and its descendants in a sentence

    
### Function `phrasesToStr` {#id}




>     def phrasesToStr(
>         spo
>     )


Returns a string from a spo tuple

    
### Function `prep` {#id}




>     def prep(
>         tokens
>     )


Returns the preposition of a sentence

    
### Function `preps` {#id}




>     def preps(
>         tokens
>     )


Returns a list of prepositions in a sentence

    
### Function `preps_descendants` {#id}




>     def preps_descendants(
>         token,
>         skip=[]
>     )


Returns a list of prepositions and their descendants in a sentence

    
### Function `root` {#id}




>     def root(
>         tokens
>     )


Returns the first root token, in tokens, or None

    
### Function `subj` {#id}




>     def subj(
>         tokens
>     )


Returns the first subject of a sentence, or None

    
### Function `verb_ancestors` {#id}




>     def verb_ancestors(
>         token
>     )


Returns ancestors which are verbs

    
### Function `verb_descendants` {#id}




>     def verb_descendants(
>         tokens,
>         skip=[]
>     )


Returns a list of verbs and their descendants in a sentence

    
### Function `verb_subj_ancestors` {#id}




>     def verb_subj_ancestors(
>         token
>     )


Returns verb-subjects from ancestors

    
### Function `verbs` {#id}




>     def verbs(
>         tokens
>     )


Returns a list of verbs in a sentence




    
# Module `depcy.split` {#id}

This module contains functions to split the spacy dependency trees.
Every function takes a spacy doc as input and returns a spacy doc as output.

In python console use it like this:
```python-repl
>>> import spacy
>>> nlp = spacy.load("en_core_web_sm")
```


```python-repl
>>> from depcy.utils import tree_view
```


```python-repl
>>> doc = nlp("Tom plays tennis and Jo plays socker")  
>>> print(splitIntoSubtrees(doc))
Tom plays tennis. Jo plays socker.
```


```python-repl
>>> doc1 = nlp("The soldier and the teacher walk home and take supper and drink wine.")
>>> print(splitIntoSubtrees(doc1))
The soldier and the teacher walk home. They take supper. They drink wine.
```


```python-repl
>>> doc2 = nlp("The soldier and the teacher walk to the pub, which was closed.")
>>> print(splitIntoSubtrees(doc2))
The soldier and the teacher walk to the pub. which was closed.
```





    
## Functions


    
### Function `fillPhrase` {#id}




>     def fillPhrase(
>         context,
>         phrase
>     )




    
### Function `fillPhrases` {#id}




>     def fillPhrases(
>         phrases
>     )




    
### Function `splitIntoSubtrees` {#id}




>     def splitIntoSubtrees(
>         doc,
>         fill_mask=True
>     )


Split a sentence into subtrees headed by a verb. if noFill is False, the <mask> is used instead of the subject.

    
### Function `splitSentAtDep` {#id}




>     def splitSentAtDep(
>         doc,
>         depSplit='ccomp'
>     )


Split a sentence at a given dependency.

    
### Function `splitSentConj` {#id}




>     def splitSentConj(
>         doc,
>         depSplit='conj'
>     )


Split a sentence with a top level conjunction into two sentences.

    
### Function `splitUp` {#id}




>     def splitUp(
>         doc
>     )


a simple split up a sentence into pieces

    
### Function `split_sentences` {#id}




>     def split_sentences(
>         doc
>     )


Split sentences on punctuation




    
# Module `depcy.utils` {#id}

This module contains functions to split the spacy dependency trees.
Every function takes a spacy doc as input and returns a spacy doc as output.

In python console use it like this:
> import spacy
> nlp = spacy.load("en_core_web_sm")
> from depcy.merge import merge_prepositions, merge_compound_nouns, merge_phrases, merge_punct
> from depcy.transform import tree_view

> doc = nlp("Tom plays tennis and Jo plays socker")
> splitSentConj(doc,depSplit="ccomp")




    
## Functions


    
### Function `annotate_depth` {#id}




>     def annotate_depth(
>         doc
>     )


Annotate the depth of each token in the dependency tree

!! You need to set the extension depth like this !!

> Token.set_extension("depth", default = 0)

    
### Function `pretty` {#id}




>     def pretty(
>         doc
>     )


Petty print a spacy doc

    
### Function `print_tree` {#id}




>     def print_tree(
>         token,
>         indent=0,
>         last=True,
>         prefix=''
>     )


Prints a dependency tree starting from a token

    
### Function `to_dep_dict` {#id}




>     def to_dep_dict(
>         doc
>     )


convert a spacy doc to a dictionary

    
### Function `tree_view` {#id}




>     def tree_view(
>         doc
>     )


Print the tree structure of the sentence.



-----
Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>).
