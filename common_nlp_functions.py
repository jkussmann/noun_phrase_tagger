"""
This module contains common nlp functions
"""

import spacy
from nltk.tokenize import RegexpTokenizer

SPACY_NLP = spacy.load("en_core_web_sm")

TOKENIZER = RegexpTokenizer(r"\w+")
