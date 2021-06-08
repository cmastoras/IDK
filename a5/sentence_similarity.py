import statistics
import csv, string
import numpy as np
from scipy.stats import spearmanr
from embeddings import Embeddings
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import math


def read_sts(infile = 'data/sts-dev.csv'):
    sts = {}
    for row in csv.reader(open(infile), delimiter='\t'):
        if len(row) < 7: continue
        val = float(row[4])
        s1, s2 = row[5], row[6]
        sts[s1, s2] = val / 5.0
    return sts

def calculate_sentence_embedding(embeddings, sent, weighted = False):
    """
    Calculate a sentence embedding vector.

    If weighted is False, this is the elementwise sum of the constituent word vectors.
    If weighted is True, multiply each vector by a scalar calculated
    by taking the log of its word_rank. The word_rank value is available
    via a dictionary on the Embeddings class, e.g.:
       embeddings.word_rank['the'] # returns 1

    In either case, tokenize the sentence with the `word_tokenize` function,
    lowercase the tokens, and ignore any words for which we don't have word vectors. 

    Parameters
    ----------
    sent : str
        A sentence for which to calculate an embedding.

    weighted : bool
        Whether or not to use word_rank weighting.

    Returns
    -------
    np.array of floats
        Embedding vector for the sentence.
    
    """
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    no_punc = ""
    for char in sent:
        if char not in punctuations:
            no_punc = no_punc + char
    first_list = word_tokenize(sent)
    #first_list = no_punc.split(''!()-[]{};:'"\,<>./?@#$%^&*_~')
    #print(first_list)
    word_list = []
    for word in first_list:
        word_list.append(word.lower())
    done = False
    count = 0
    
    #while done == False:
     #   if word_list[count] in embeddings:
      #      sen_vec = np.zeros(len(embeddings[word_list[count]]))
       #     #print(str(sen_vec))
        #    done == True
       # else:
         #   count += 1
    sen_vec = np.zeros(50)
    
    if weighted == False:
        for word in word_list:
            if word in embeddings:
                word_vec = np.array(embeddings[word])
                sen_vec = np.add(sen_vec,word_vec)
    else:
        for word in word_list:
            if word in embeddings:
                word_vec = np.array(embeddings[word])
                importance = math.log(embeddings.word_rank[word])
                dirty_word_vec = word_vec*importance
                sen_vec = np.add(sen_vec,dirty_word_vec)
    # >>> YOUR ANSWER HERE
    return sen_vec
    # >>> END YOUR ANSWER



def score_sentence_dataset(embeddings, dataset, weighted = False):
    """
    Calculate the correlation between human judgments of sentence similarity
    and the scores given by using sentence embeddings.

    Parameters
    ----------
    dataset : dictionary of the form { (sentence, sentence) : similarity_value }
        Dataset of sentence pairs and human similarity judgments.
    
    weighted : bool
        Whether or not to use word_rank weighting.

    Returns
    -------
    float
        The Spearman's Rho ranked correlation coefficient between
        the sentence emedding similarities and the human judgments.     
    """
    gold_vals = []
    sen_vals = []
    for thing in dataset:
        gold_vals.append(dataset[thing])
        val1 = calculate_sentence_embedding(embeddings,thing[0],weighted)
        val2 = calculate_sentence_embedding(embeddings,thing[1],weighted)
        val3 = embeddings.cosine_similarity(val1,val2)
        sen_vals.append(val3)
    # >>> YOUR ANSWER HERE
    number = spearmanr(gold_vals,sen_vals)
    sen_score = number[0]
    return sen_score
    # >>> END YOUR ANSWER

if __name__ == '__main__':
    embeddings = Embeddings()
    sts = read_sts()
    values = calculate_sentence_embedding(embeddings,"Over , the rainbow ?")
    print(statistics.mean(values))
    print('STS-B score without weighting:', score_sentence_dataset(embeddings, sts))
    print('STS-B score with weighting:', score_sentence_dataset(embeddings, sts, True))
