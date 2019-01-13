# Noun Phrase Tagger
This is a noun phrase tagger using NLTK, Spacy, and Stanford Core NLP. The results of each one is consolidated to include any tags ommitted by one of the taggers. If there is disagreement among the taggers for a word, the majority is used. If all 3 taggers disagree, Spacy is used.

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

## Testing

To run unit tests on the code, open a command line window and change to the directory where the code is located.
The test waits for 2 minutes to give the Stanford Core NLP server time to get started and initialize.
The wait time may have to be lengthened depending on system speed. Warnings have been suppressed due to file
open and socket warnings. The warning suppression will be removed as the tests are improved.

```
C:\noun_phrase_tagger>python test_np_unittest.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.236s

OK
```

## Author

* **John Kussmann** - *Initial work*
