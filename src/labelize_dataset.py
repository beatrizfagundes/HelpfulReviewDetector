#
# Author: Beatriz Fagundes
#
# Transform the helpful votes (in numbers) to class labels "helpful" and
# "not helpful" based on the following approach:
#   if helpfulVotes / totalVotes >= 0.7 then class = "helpful"
#   else if helpfulVotes / totalVotes <= 0.3 then class = "not helpful"
#   else discard the instance (for now)
#

import sys
import csv
import logging
from csv_converter import save_csv
import os

def read_csv(dataset):
    corpus = []
    keys = []
    num_line = 0
    with open(dataset, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            if num_line == 0:
                # header
                keys = row
                num_line += 1
            else:
                instance = {}
                for i in range(len(row)):
                    instance[keys[i]] = row[i]
                corpus.append(instance)
    return corpus


def labelize(corpus):
    labelized_corpus = []
    for review in corpus:
        total = float(review['totalVotes'])
        if total != 0:
            helpfulness_ratio = float(review['helpfulVotes']) / total
            if helpfulness_ratio >= 0.7:
                review['reviewClass'] = 'helpful'
                labelized_corpus.append(review)
            elif helpfulness_ratio <= 0.3:
                review['reviewClass'] = 'not_helpful'
                labelized_corpus.append(review)
    return labelized_corpus


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

    corpus = read_csv(dataset)
    labelized_corpus = labelize(corpus)
    save_csv(labelized_corpus, dataset.replace('.csv', '_label.csv'))


main()
