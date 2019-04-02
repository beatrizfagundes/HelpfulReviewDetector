# -*- coding: utf-8 -*-
#
# Author: Beatriz Fagundes
#
# Converts a dataset to a CSV file
#
# usage: python csv_converter.py [options] [file or directory]
# OPTIONS:
# json  |
# dir   |
# e.g.: python csv_converter.py json /path/to/json/file
# e.g.: python csv_converter.py dir /path/to/directory/with/text/data
#

import sys
import os
import csv
import json
import gzip
import logging


# This method is not used here internally but it is used externally
def read_csv(dataset):
    corpus = []
    keys = []
    num_line = 0
    with open(dataset, newline='') as csvfile:
        logging.info('Reading CSV file...')
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
    logging.info('Number of documents: %s' % str(len(corpus)))
    return corpus


def save_csv(corpus, outfile):
    logging.info('Number of documents: %s' % str(len(corpus)))
    logging.info('Creating CSV file...')
    f = open(outfile, 'w')
    try:
        writer = csv.writer(f)
        colnames = tuple(corpus[0].keys())
        writer.writerow(colnames)
        for instance in corpus:
            writer.writerow(tuple(instance.values()))
    finally:
        f.close()
    logging.info('Finished! Your file %s has been created in the current \
directory.' % outfile)


def dir2csv(dataset_folder):
    corpus = []
    # traverse folders
    for root, subdirs, files in os.walk(dataset_folder):
        for subdir in subdirs:
            full_subdir_path = os.path.join(root, subdir)
            for filename in os.listdir(full_subdir_path):
                full_file_path = os.path.join(full_subdir_path, filename)
                with open(full_file_path, 'rb') as f:
                    comment = f.read().decode(errors='ignore')
                    comment = comment.replace('_x000D_', '')
                    # join all sentences of a comment into one single sentence
                    instance_to_save = {
                        'reviewText': comment,
                        'reviewClass': str(subdir)
                    }
                    corpus.append(instance_to_save)

    save_csv(corpus, dataset_folder + '.csv')


"""
Parse reviews like the ones available at the following URL:
http://jmcauley.ucsd.edu/data/amazon/
"""


def json2csv(dataset, compressed):
    corpus = []
    f = gzip.open(dataset, 'r') if compressed else open(dataset, 'r')
    try:
        for json_instance in f:
            original = json.loads(json_instance)
            instance_to_save = {
                'reviewerID': original['reviewerID'],
                'reviewText': original['reviewText'],
                'helpfulVotes': int(original['helpful'][0]),
                'totalVotes': int(original['helpful'][1]),
                'starRating': original['overall'],
                'reviewSummary': original['summary'],
                'reviewDate': original['reviewTime']
            }
            corpus.append(instance_to_save)
    finally:
        f.close()

    save_csv(corpus, dataset.replace('.json', '.csv'))


def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='LOG_csv_converter.log')
    logging.info('Starting CSV converter...')
    if len(sys.argv) < 3:
        logging.info('ERROR! Missing params, you must follow the usage:')
        logging.info("python csv_converter.py [option]='json' or 'dir' [file \
or directory path]")
        return
    option = sys.argv[1]
    dataset = sys.argv[2]
    logging.info('with option: %s' % option)
    logging.info('with dataset: %s' % dataset)
    # check if the file is compressed by gzip
    compressed = dataset.lower().endswith('.gz')
    if option == 'json':
        json2csv(dataset, compressed)
    elif option == 'dir':
        dir2csv(dataset)


main()
