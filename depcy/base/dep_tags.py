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
  This file contains a dictionary of dependency tags, their descriptions, examples and prolog categories.
"""

test_database = {}

# English dependency tags, descriptions, examples and prolog categories: see https://downloads.cs.stanford.edu/nlp/software/dependencies_manual.pdf for more details
tagged_examples = {
  'acl'     : ('clausal modifier of noun','His decision, to accept the job offer, surprised everyone.','None','clausal'),
  'acomp'   : ('adjectival complement','She is nice.','She *is* **nice**.','comp'), # causal
  'advcl'   : ('adverbial clausal modifier','She left when the sun went down.','She *left* when the sun **went** down.','clausal'),
  'advmod'  : ('adverbial modifier','He runs quickly.','He *runs* **quickly**.','pretag'),
  'agent'   : ('agent','The book was written by John.','The book was *written* **by** John.','prep'),
  'amod'    : ('adjectival modifier','She has a blue car.','She has a **blue** *car*.','adj'),
  'appos'   : ('appositional modifier','My friend Alice, a doctor, is visiting today.','My *friend* **Alice** , a **doctor** , is visiting today.','comp'),
  'attr'    : ('attribute','Daniel is a smart clever professor.','Daniel *is* a smart clever **professor**.','entity'),
  'aux'     : ('auxiliary','He is running.','He **is** *running*.','pretag'), # pretag
  'auxpass' : ('passive auxiliary','Kennedy has been killed.','Kennedy has **been** *killed*.','pretag'),
  'case'    : ('case marking','He went to the store.','None','cond'),
  'cc'      : ('coordinating conjunction','She likes coffee and tea.','She likes *coffee* **and** tea.','pretag'),
  'ccomp'   : ('clausal complement','I think you should go.','I *think* you should **go**.','clausal'),
  'compound': ('compound','She walked to downtown Bern.','She walked to **downtown** *Bern*.','comp'),
  'conj'    : ('conjunct','I like to swim and play tennis.','I like to *swim* and **play** tennis.','conj'),
  'cop'     : ('copula','Bill is an honest man.','None','cond'),
  'csubj'   : ('clausal subject','What she said makes sense.','What she **said** *makes* sense.','clausal'),
  'csubjpass'   : ('clausal passive subject','That the law was broken was known by everyone.','None','clausal'),
  'dative'  : ('dative','She gave him a gift.','She *gave* **him** a gift.','entity'),
  'dep'     : ('dependent','He spoke about his trip.','None','cond'),
  'det'     : ('determiner','She ate the apple.','She ate **the** *apple*.','det'),
  'dobj'    : ('direct object','She bought a book.','She *bought* a **book**.','entity'),
  'expl'    : ('expletive','There are many books on the shelf.','**There** *are* many books on the shelf.','cond'),
  'intj'    : ('interjection','Iguazu is in Argentina :)','None','cond'),
  'mark'    : ('marker','He says that you like to swim.','He says **that** you *like* to swim.','pretag'),
  'meta'    : ('meta modifier','He told me, "I will come".','None','cond'),
  'neg'     : ('negation modifier','He did not go to the party.','He did **not** *go* to the party.','pretag'),
  'nmod'    : ('nominal modifier','She lives in New York.','None','cond'),
  'npadvmod': ('noun phrase as adverbial modifier','I will see you next week.','None','cond'),
  'nsubj'   : ('nominal subject','She likes to read.','**She** *likes* to read.','entity'),
  'nsubjpass': ('passive nominal subject','He was caught.','**He** was *caught*.','entity'),
  'nummod'  : ('numeric modifier','I ate two apples.','I ate **two** *apples*.','num'),
  'oprd'    : ('object predicate','She made him her husband.','None','cond'),
  'parataxis': ('parataxal clausal side by side','The guy, John said, left early in the morning.','The guy , John **said** , *left* early in the morning.','clausal'),
  'pcomp'   : ('prepositional clausal complement','We have no information on whether users are at risk.','We have no information *on* whether users **are** at risk.','clausal'),
  'pobj'    : ('object of preposition','She sat on the chair.','She sat *on* the **chair**.','entity'),
  'poss'    : ('possession modifier','This is my car.','This is **my** *car*.','adj'),
  'preconj' : ('pre-correlative conjunction','Both my brother and sister came.','**Both** my *brother* and sister came.','det'),
  'predet'  : ('predeterminer','All the students passed the exam.','**All** the *students* passed the exam.','det'),
  'prep'    : ('prepositional modifier','She went to the park.','She *went* **to** the park.','prep'),
  'prt'     : ('particle','They shut down the station.','They *shut* **down** the station.','pretag'),
  'punct'   : ('punctuation','Does he like me?','Does he *like* me **?**','cond'),
  'quantmod': ('quantifier modifier','More than 200 people came to the party.','More **than** *200* people came to the party.','cond'),
  'relcl'   : ('relative clausal modifier','He met the woman who lives next door.','He met the *woman* who **lives** next door.','clausal'),
  'xcomp'   : ('open clausal complement','He says that you like to swim.','He says that you *like* to **swim**.','clausal')
}
        
# extract helper sets from above dictionary for easier access
cats = {v[3] for v in tagged_examples.values()}
# for a translation to prolog we work with the following categories
conds = {k for k,v in tagged_examples.items() if v[3] == 'cond'}
preps = {k for k,v in tagged_examples.items() if v[3] == 'prep'}
negs = {k for k,v in tagged_examples.items() if v[3] == 'neg'}
conjs = {k for k,v in tagged_examples.items() if v[3] == 'conj'}
dets = {k for k,v in tagged_examples.items() if v[3] == 'det'}
entities = {k for k,v in tagged_examples.items() if v[3] == 'entity'}
clausals = {k for k,v in tagged_examples.items() if v[3] == 'clausal'}

# a helper dictionary of dependency tags and their corresponding categories
dep_dict = {cat: {k for k,v in tagged_examples.items() if v[3] == cat} for cat in cats}

# an alternative categorisation of dependency tags into subject, object, indirect object, and supplementary
subj_tags = {'nsubj', 'nsubjpass', 'csubj', 'csubjpass','expl'}
obj_tags  = {'dobj', 'pobj','attr','ccomp','acomp','xcomp','oprd'}
iobj_tags = {'dative','npadvmod'}
suppl_tags = {'acl', 'advcl', 
         'advmod', 'agent', 'amod', 'appos', 'attr', 'aux', 'auxpass', 'case', 'cc', 
         'ccomp', 'compound', 'conj', 'cop', 'dative', 'dep', 'det', 'expl', 'intj', 
         'mark', 'meta', 'neg', 'nmod', 'npmod', 'nummod', 'oprd', 'parataxis', 'pcomp',
         'poss', 'preconj', 'predet', 'prep', 'prt', 'punct', 'quantmod', 'relcl', 'xcomp'}

