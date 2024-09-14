import spacy
from spacy.language import Language
from spacy.tokens import Doc

# Custom sentence boundary detection function
@Language.component("custom_boundaries")
def set_custom_boundaries(doc: Doc) -> Doc:
    for token in doc[:-1]:
        if token.text == "apples":  # Custom rule: split after 'apples'
            doc[token.i + 1].is_sent_start = True
    return doc

# Load spaCy model
nlp = spacy.load("en_core_web_trf")

# Add the sentencizer to the pipeline
nlp.add_pipe("sentencizer")

# Add custom sentence boundary detector to the pipeline using the registered name
nlp.add_pipe("custom_boundaries", before="parser")

text = "I like apples I like bananas"

doc = nlp(text)

for sentence in doc.sents:
    print(sentence.text)
