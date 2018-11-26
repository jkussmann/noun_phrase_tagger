# Noun Phrase Tagger
This is a part of speech tagger using NLTK, Spacy, and Stanford Core NLP. The results of each one is consolidated to include any tags ommitted by one of the taggers. If there is disagreement among the taggers for a word, the majority is used. If all 3 taggers disagree, Spacy is used.

## Getting Started

This code is initially written to run on a Windows 10 environment. The program is run from the command line and any IDE can be used.

### Prerequisites

What things you need to install the software and how to install them
* Python 3 (https://www.python.org/downloads/windows/)
* NLTK (https://www.nltk.org/)
* Spacy (https://spacy.io/)
* Stanford CoreNLP (https://stanfordnlp.github.io/CoreNLP/)

## Running the code

Open a command line window and change to the directory the code is located

```
c:\noun_phrase_tagger>python main.py
Initializing CoreNLP....

Enter a sentence: The little yellow dog chased the boy in the red car.

Stanford Noun Phrases:
The little yellow dog, the boy, the red car

NLTK Noun Phrases:
The little yellow dog, the boy, the red car

Spacy Noun Phrases:
The little yellow dog, the boy, the red car

Consolidated Noun Phrases:
The little yellow dog, the boy, the red car

Enter a sentence: end
Ending Program ...

c:\noun_phrase_tagger>
```

## Author

* **John Kussmann** - *Initial work*
