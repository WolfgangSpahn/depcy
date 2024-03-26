"""
    Annotate a spacy doc with html tags for entities

    Example:
    >>> import spacy
    >>> from depcy.annotate import annotate
    >>> nlp = spacy.load("en_core_web_sm")
    >>> doc = nlp("Energy is a measure of a system's ability to do work or produce change. It exists in various forms, such as kinetic energy, potential energy, thermal energy, and others. Energy can be transformed from one form to another but cannot be created or destroyed, a principle known as the conservation of energy.")
    >>> print(annotate(doc))
"""


from depcy.base.merge import merge_all
from depcy.extract import nouns_propns

def mark(text, entities):
    """
    Mark entities in text
    """
    for entity in entities:
        text = text.replace(entity, f"<mark class='...'>{entity}<sup>...</sup></mark>")
    return text

def annotate(doc):
    """Create an annotated html representation of a spacy doc"""
    doc = merge_all(doc)
    docs = [sent.as_doc() for sent in doc.sents]

    result = ""
    for doc in docs:
        entities = [t.text for t in nouns_propns(doc)]
        print(entities)
        result += mark(doc.text, entities)

    return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()
