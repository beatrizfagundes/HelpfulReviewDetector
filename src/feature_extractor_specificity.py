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
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from joblib import Parallel, delayed
#from sklearn.externals.joblib import Parallel, delayed
import itertools
import pandas as pd


def specificity_features(review, nlp):
    specif_degree = 0
    num_specif = 0
    num_gen = 0
    # find sentences and store them in a temp file
    review = review.replace('"', '')
    num_sents = 0
    f = open('sents.txt', 'w')
    try:
        for sentence in nlp(review).sents:
            num_sents += 1
            f.write(str(sentence)+'\n')
    finally:
        f.close()

    if num_sents == 0:
        return (0, 0, 0)
    # running SPECITELLER
    full_cmd = 'python3 test.py --test_data sents.txt'
    # supress command output
    full_cmd += ' > /dev/null 2>&1'
    os.system(full_cmd)
    # handles the MARGOT output file
    f = open('predictions.txt', 'r')
    try:
        for tensor in f:
            tensor = tensor.replace('tensor(', '')
            degree = float(tensor.replace(')', ''))
            if degree < 0.5:
                num_gen += 1
            else:
                num_specif += 1
            specif_degree += degree
    finally:
        f.close()
    return (float(specif_degree)/float(num_sents),
            float(num_specif)/float(num_sents),
            float(num_gen)/float(num_sents))


def extract_features(corpus):
    features_names = ['SpecifDegree', 'SpecifSents', 'GenSents']
    for f in features_names:
        corpus[f] = 0.0
    count = 0
    nlp = spacy.load("en_core_web_sm")
    for index, row in corpus.iterrows():
        count += 1
        print(str(count))
        specif_degree, num_specif, num_gen = specificity_features(row.reviewText, nlp)
        corpus.loc[index, 'SpecifDegree'] = specif_degree
        corpus.loc[index, 'SpecifSents'] = num_specif
        corpus.loc[index, 'GenSents'] = num_gen
#    import ipdb; ipdb.set_trace()
    return corpus[['SpecifDegree', 'SpecifSents', 'GenSents', 'reviewClass']].copy()


def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='feature_extractor_specificity.log')
    logging.info('Starting Feature Extractor...')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python feature_extractor_specificity.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)

    corpus = pd.read_csv(dataset)
    previous_dir = os.getcwd()
    full_speciteller_path = '../lib/speciteller/Domain-Agnostic-Sentence-Specificity-Prediction'
    os.chdir(full_speciteller_path)
    preprocessed = extract_features(corpus)
    logging.info('Storing the preprocessed dataset')
    os.chdir(previous_dir)
    preprocessed.to_csv(dataset.replace('label', 'spec'), header=True, index=None)


main()
