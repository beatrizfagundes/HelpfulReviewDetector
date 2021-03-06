#
# Author: Beatriz Fagundes
#
#

import sys
import csv
import logging
import json
import math
import os
import spacy
#from joblib import Parallel, delayed
from sklearn.externals.joblib import Parallel, delayed
import itertools
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def tokenize(review):
    tokens = []
    nlp = spacy.load("en_core_web_sm")
    preprocessed_review = nlp(review, disable=['parser', 'ner', 'tagger'])
    for token in preprocessed_review:
#        if not token.is_stop and not token.is_punct and not token.is_digit and not token.is_space and not token.is_bracket and not token.is_quote and not token.like_url and not token.like_num and not token.like_email:
        if not token.is_stop and not token.is_punct and not token.is_space and not token.is_bracket and not token.is_quote and not token.like_num:
            tokens.append(token.lower_)
    return ' '.join(tokens)


def extract_features(corpus):
    # tokenize reviews
    corpus = corpus.dropna()
    print(str(corpus.shape[0]))
    logging.info('Number of valid documents: %s' % str(corpus.shape[0]))
    corpus['tokens'] = Parallel(n_jobs=-1)(delayed(tokenize)(review) for review in corpus.reviewText)
    corpus_tokens = corpus.tokens
    corpus_class = corpus.reviewClass
    del corpus
    # calculate IDF
    tfidf_vec = TfidfVectorizer(min_df=.01, max_df=.6, binary=True)
    X = tfidf_vec.fit_transform(corpus_tokens)
    features_names = tfidf_vec.get_feature_names()
    logging.info('Number of features extracted: %s' % str(len(features_names)))
    print(str(len(features_names)))
    # transform table with tfidf weights to pandas dataframe
    df_tfidf = pd.DataFrame(X.toarray(), columns=features_names)
    df_tfidf['reviewClass'] = corpus_class
    return df_tfidf


def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='feature_extractor_idf.log')
    logging.info('Starting Feature Extractor...')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python feature_extractor.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)

    corpus = pd.read_csv(dataset)
    preprocessed = extract_features(corpus)
    logging.info('Storing the preprocessed dataset...')
    print('Storing the preprocessed dataset...')
    preprocessed.to_csv(dataset.replace('label', 'idf'), header=True, index=None)


main()
