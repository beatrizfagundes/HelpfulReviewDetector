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
from csv_converter import save_csv, read_csv
import os


def labelize(corpus):
    labelized_corpus = []
    review_only = []
    count = 1
    for review in corpus:
        total = float(review['totalVotes'])
        if total != 0:
            review['ID'] = count
            helpfulness_ratio = float(review['helpfulVotes']) / total
            if helpfulness_ratio >= 0.7:
                review['reviewClass'] = 'helpful'
                labelized_corpus.append(review)
                review_only.append(review['reviewText'])
                count += 1
            elif helpfulness_ratio <= 0.3:
                review['reviewClass'] = 'not_helpful'
                labelized_corpus.append(review)
                review_only.append(review['reviewText'])
                count += 1
    return (labelized_corpus, review_only)


def save_txt(reviews, outfile):
    f = open(outfile, 'w')
    try:
        for r in reviews:
            f.write(r + '\n')
    finally:
        f.close()


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
    labelized_corpus, review_only = labelize(corpus)
    save_csv(labelized_corpus, dataset.replace('.csv', '_label.csv'))
    save_txt(review_only, dataset.replace('.csv', '.txt'))


main()
