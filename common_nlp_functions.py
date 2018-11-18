import spacy
spacy_nlp = spacy.load('en_core_web_sm')

from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')