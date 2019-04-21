#
# Author: Beatriz Fagundes
#
#

import sys
import logging
import random
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from joblib import Parallel, delayed
#from sklearn.externals.joblib import Parallel, delayed
import itertools
import pandas as pd


def split_sentences(review, nlp):
    review = review.replace('"', '')
    review_sents = []
    for sentence in nlp(review).sents:
        review_sents.append(str(sentence))
    return review_sents


def extract_sentences(corpus):
    # tokenize reviews
    corpus = corpus.dropna()
    print(str(corpus.shape[0]))
    logging.info('Number of valid documents: %s' % str(corpus.shape[0]))
    # sample documents from corpus
    corpus = corpus.sample(n=2000)
    print(str(corpus.shape[0]))
    logging.info('Number of sampled documents: %s' % str(corpus.shape[0]))

    nlp = spacy.load("en_core_web_sm")
    sentences = Parallel(n_jobs=-1)(delayed(split_sentences)(review, nlp) for review in corpus.reviewText)
    print('Finished finding sentences')
    del corpus
    all_sentences = list(itertools.chain(*sentences))
    print(str(len(all_sentences)))
    if len(all_sentences) > 4300:
        all_sentences = random.sample(all_sentences, 4300)
    df_sents = pd.DataFrame(all_sentences, columns=['sentences'])
    return df_sents


def main():
    random.seed(2)
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='get_sentences_sample.log')
    logging.info('Starting...')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python get_sentence_sample.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)

    corpus = pd.read_csv(dataset)
    sentences = extract_sentences(corpus)
    logging.info('Storing the sentences...')
    print('Storing the sentences...')
    sentences.to_csv(dataset.replace('.txt', '_train.txt'), header=False, index=None)


main()
