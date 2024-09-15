import nltk
from nltk.tokenize import PunktSentenceTokenizer

text = "this is a sentence here is another one without any punctuation"

tokenizer = PunktSentenceTokenizer()
sentences = tokenizer.tokenize(text)
print(sentences)
