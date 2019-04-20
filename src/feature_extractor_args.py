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


def argument_features(review):
    num_non_args = 0 # number of non-argumentative sentences
    num_claims = 0
    num_evidences = 0
    # Words that belong both to a claim and to a piece of evidence
    num_claim_evidence = 0

    # running MARGOT
    run_margot_cmd = './run_margot.sh'
    output_path = '.' # current directory
    review = review.replace('"', '')
    input_file = '"' + review + '"'
    full_cmd = run_margot_cmd + ' ' + input_file + ' ' + output_path
    # supress command output
    full_cmd += ' > /dev/null 2>&1'
    os.system(full_cmd)
    # handles the MARGOT output file
    f = open('OUTPUT.json', 'r')
    try:
        for json_instance in f:
            doc = json.loads(json_instance)['document']
            for sent in doc:
                if 'evidence' in sent:
                    num_evidences += 1
                if 'claim' in sent:
                    num_claims += 1
                if 'claim_evidence' in sent:
                    num_claim_evidence += 1
                if not 'evidence' in sent and not 'claim' in sent and not 'claim_evidence' in sent:
                    num_non_args += 1
    finally:
        f.close()
    total_sents = num_evidences + num_claims + num_claim_evidence + num_non_args
    if total_sents == 0:
        return (0, 0, 0, 0)
    else:
        return (float(num_evidences)/float(total_sents),
                float(num_claims)/float(total_sents),
                float(num_claim_evidence)/float(total_sents),
                float(num_non_args)/float(total_sents))


def extract_features(corpus):
    features_names = ['Evidences', 'Claims', 'ClaimEvidence', 'NonArgs']
    for f in features_names:
        corpus[f] = 0.0
    count = 0
    print(corpus.head())
    for index, row in corpus.iterrows():
        count += 1
        print(str(count))
        num_evidences, num_claims, num_claim_evidence, num_non_args = argument_features(row.reviewText)
        corpus.loc[index, 'Evidences'] = num_evidences
        corpus.loc[index, 'Claims'] = num_claims
        corpus.loc[index, 'ClaimEvidence'] = num_claim_evidence
        corpus.loc[index, 'NonArgs'] = num_non_args
#    tokens_per_review = Parallel(n_jobs=-1)(delayed(extract_tokens)(review_info) for review_info in corpus)
#    import ipdb; ipdb.set_trace()
    return corpus[['Evidences', 'Claims', 'ClaimEvidence', 'NonArgs', 'reviewClass']].copy()


def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='feature_extractor.log')
    logging.info('Starting Feature Extractor...')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python feature_extractor.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)

    corpus = pd.read_csv(dataset, nrows=5)
    previous_dir = os.getcwd()
    full_margot_path = '../lib/margot-modified/predictor'
    os.chdir(full_margot_path)
    preprocessed = extract_features(corpus)
    logging.info('Storing the preprocessed dataset')
    os.chdir(previous_dir)
    preprocessed.to_csv(dataset.replace('label', 'args'), header=True, index=None)


main()
