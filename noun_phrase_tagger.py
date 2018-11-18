import pickle
import random
import os
import common_nlp_functions as cnf

from collections import Iterable
from nltk import ChunkParserI, ClassifierBasedTagger, word_tokenize, pos_tag
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import conll2000
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.tag.stanford import CoreNLPPOSTagger
from difflib import SequenceMatcher

stPOS = CoreNLPPOSTagger(url='http://localhost:9000')

model_path = "models/"

def get_similarity_score(string1, string2):    
    return SequenceMatcher(None, string1, string2).ratio()
 
def features(tokens, index, history):
    """
    `tokens`  = a POS-tagged sentence [(w1, t1), ...]
    `index`   = the index of the token we want to extract features for
    `history` = the previous predicted IOB tags
    """
 
    # init the stemmer
    stemmer = SnowballStemmer('english')
 
    # Pad the sequence with placeholders
    tokens = [('__START2__', '__START2__'), ('__START1__', '__START1__')] + list(tokens) + [('__END1__', '__END1__'), ('__END2__', '__END2__')]
    history = ['__START2__', '__START1__'] + list(history)
 
    # shift the index with 2, to accommodate the padding
    index += 2
 
    word, pos = tokens[index]
    prevword, prevpos = tokens[index - 1]
    prevprevword, prevprevpos = tokens[index - 2]
    nextword, nextpos = tokens[index + 1]
    nextnextword, nextnextpos = tokens[index + 2]
 
    return {
        'word': word,
        'lemma': stemmer.stem(word),
        'pos': pos,
 
        'next-word': nextword,
        'next-pos': nextpos,
 
        'next-next-word': nextnextword,
        'nextnextpos': nextnextpos,
 
        'prev-word': prevword,
        'prev-pos': prevpos,
 
        'prev-prev-word': prevprevword,
        'prev-prev-pos': prevprevpos,
    }
 
class ClassifierChunkParser(ChunkParserI):
    def __init__(self, chunked_sents, **kwargs):
        assert isinstance(chunked_sents, Iterable)
 
        # Transform the trees in IOB annotated sentences [(word, pos, chunk), ...]
        chunked_sents = [tree2conlltags(sent) for sent in chunked_sents]
 
        # Transform the triplets in pairs, make it compatible with the tagger interface [((word, pos), chunk), ...]
        def triplets2tagged_pairs(iob_sent):
            return [((word, pos), chunk) for word, pos, chunk in iob_sent]
			
        chunked_sents = [triplets2tagged_pairs(sent) for sent in chunked_sents]
 
        self.feature_detector = features
        self.tagger = ClassifierBasedTagger(
            train = chunked_sents,
            feature_detector = features,
            **kwargs)
 
    def parse(self, tagged_sent):
        chunks = self.tagger.tag(tagged_sent)
 
        # Transform the result from [((w1, t1), iob1), ...] 
        # to the preferred list of triplets format [(w1, t1, iob1), ...]
        iob_triplets = [(w, t, c) for ((w, t), c) in chunks]
 
        # Transform the list of triplets to nltk.Tree format
        return conlltags2tree(iob_triplets)
		
def train_chunker():
    print ('Training chunker...')    
	
    shuffled_conll_sents = list(conll2000.chunked_sents())
    random.shuffle(shuffled_conll_sents)
    train_sents = shuffled_conll_sents[:int(len(shuffled_conll_sents) * 0.9)]
    test_sents = shuffled_conll_sents[int(len(shuffled_conll_sents) * 0.9 + 1):]

    classifier_chunker = ClassifierChunkParser(train_sents)
    print (classifier_chunker.evaluate(test_sents))
	
	# save model to pickle file as binary
    file_name = model_path + 'chunk_model.pkl'
    with open(file_name, 'wb') as fout:
        pickle.dump(classifier_chunker, fout)
		
    print ('model written to: ' + file_name)
    return classifier_chunker
		
def get_chunker():
    # check if models exist, if not run training    
    if(os.path.isfile(model_path + 'chunk_model.pkl') == False):
        print ('')
        print ('Creating chunk Model.....')
        chunker = train_chunker()
    else:	    
		# read the file in as binary
	    chunker = pickle.load(open(model_path + 'chunk_model.pkl', 'rb'))
		
    return chunker
 
def get_NLTK_nps(line):
    """
    Get the noun phrases using the NLTK classifier chunker
    """     
	
    chunker = get_chunker()
    tokenized_line = word_tokenize(line)
    pos_tagged_line = pos_tag(tokenized_line)
    tag_list = chunker.parse(pos_tagged_line) #tag_list is type nltk.tree.Tree 
    noun_phrase_list = []
    
    for item in tag_list.subtrees():   	 
        if item.label() in ['NP']:
            chunk_name = ' '.join([a for (a,b) in item.leaves()])	
            noun_phrase_list.append(chunk_name)			
    
    return noun_phrase_list
	
def get_stanford_nps(line):
    """
	Get noun phrases using the Stanford tagger
	"""
	
    noun_phrase_list = []	
    
    tag_list = list(stPOS.raw_parse(line))
    for item in tag_list:
        for subtree in item.subtrees():
            if subtree.label() == 'NP':
               np = ' '.join(subtree.leaves())
               noun_phrase_list.append((np))
   
    return noun_phrase_list	
	
def get_spacy_nps(line):
    """
    Use the Spacy dependency tagger to get NPs
    """
	
    tokenized_line = cnf.tokenizer.tokenize(line)
    tokenized_string = ' '.join(tokenized_line)
    tagged_line = cnf.spacy_nlp(tokenized_string)
    noun_phrase_list = []
	
    for np in tagged_line.noun_chunks:	
        noun_phrase_list.append(np.text)

    return noun_phrase_list
	
def get_noun_phrases(line):
    """
	Combine the results from Spacy, NLTK, and Stanford
	"""
	
    stanford_nps = get_stanford_nps(line)
    nltk_nps = get_NLTK_nps(line)
    spacy_nps = get_spacy_nps(line)
	
    noun_phrase_list = []

    append_item = True	
    for item1 in stanford_nps:
        for item2 in spacy_nps:			
            if (get_similarity_score(item1, item2) > .80) or (item1 in item2 or item2 in item1):
                append_item = False	

        if append_item:
            spacy_nps.append((item1))	
			
        append_item = True		

    append_item = True
    for item1 in nltk_nps:
        for item2 in spacy_nps:
            if (get_similarity_score(item1, item2) > .80) or (item1 in item2 or item2 in item1):
                append_item = False	

        if append_item:
            spacy_nps.append((item1))

        append_item = True	

    noun_phrase_list = spacy_nps 
	
    return noun_phrase_list
	
