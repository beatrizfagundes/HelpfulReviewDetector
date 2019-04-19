#
# Author: Beatriz Fagundes
#
# Transform the helpful votes (in numbers) to class labels "helpful" and
# "not helpful" based on the following approach:
#   if (helpfulVotes / totalVotes) >= 0.7 then class = "helpful"
#   else if (helpfulVotes / totalVotes) <= 0.3 then class = "not_helpful"
#   else discard the instance (for now)
#

import sys
import csv
import logging
import pandas as pd
import os
import numpy as np
from joblib import Parallel, delayed


def labelize(corpus):
    print(str(corpus.shape[0]))
    logging.info('Number of original documents: %s' % str(corpus.shape[0]))
    corpus['reviewClass'] = Parallel(n_jobs=-1)(delayed(assign_categories)(row.helpfulVotes, row.totalVotes) for index, row in corpus.iterrows())
    corpus = corpus.dropna()
    corpus.reviewClass = corpus.reviewClass.astype(int)
    print(str(corpus.shape[0]))
    logging.info('Number of labelized documents: %s' % str(corpus.shape[0]))

    return (corpus, corpus.reviewText)


def assign_categories(helpful_votes, total_votes):
    if total_votes == 0:
        return np.nan
    else:
        helpfulness_ratio = float(helpful_votes)/float(total_votes)
        if helpfulness_ratio >= 0.7:
            return 1 # return 'helpful'
        elif helpfulness_ratio <= 0.3:
            return -1 # return 'not_helpful'
        else:
            return np.nan


def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='labelize_dataset.log')
    logging.info('Starting Labelize Dataset...')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python labelize_dataset.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)

    corpus = pd.read_csv(dataset)
    labelized_corpus, review_only = labelize(corpus)
    labelized_corpus.to_csv(dataset.replace('.csv', '_label.csv'), header=True, index=None)
    review_only.to_csv(dataset.replace('.csv', '.txt'), header=True, index=None)


main()
