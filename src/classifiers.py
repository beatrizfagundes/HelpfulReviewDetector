#
# Author: Beatriz Fagundes
#
#

import sys
import logging
from csv_converter import save_csv, read_csv
import os
import random
from time import time
from sklearn import svm, naive_bayes, tree, neighbors, linear_model, metrics
from sklearn.model_selection import cross_val_score


def split_class_from_features(corpus):
    X = []
    tlabels = []
    for review in corpus:
        review_vec = []
        tlabels.append(review['reviewClass'])
        for feature in review:
            if feature != 'reviewClass':
                review_vec.append(float(review[feature]))
        X.append(review_vec)
    # transform the nominal classes to numerical classes
    tlabels_levels = list(set(tlabels))
    tlabels = [tlabels_levels.index(l) for l in tlabels]
    return (X, tlabels)


def classify(X, tlabels, result_file):
    f = open(result_file, 'w')
    try:
        clfs = [svm.LinearSVC(), naive_bayes.MultinomialNB(), linear_model.Perceptron(), linear_model.SGDClassifier()]
        for clf in clfs:
            print(clf)
            logging.info('Classifying data with %s' % clf)
            t0 = time()
            cv_accuracies = cross_val_score(clf, X, tlabels, cv=2, scoring='accuracy')
            logging.info('done in %0.3fs' % (time() - t0))
            f.write('Accuracy: %0.4f (+/- %0.2f)\n' % (cv_accuracies.mean(), cv_accuracies.std() * 2))
            t0 = time()
#            import ipdb; ipdb.set_trace()
            cv_f1 = cross_val_score(clf, X, tlabels, cv=2, scoring='f1')
            f.write('Accuracy: %0.4f (+/- %0.2f)\n' % (cv_f1.mean(), cv_f1.std() * 2))
            logging.info('done in %0.3fs' % (time() - t0))
    finally:
        f.close()


def main():
    random.seed(2)

    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='classifiers.log')
    logging.info('Starting Classification task...')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python classifiers.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)

    corpus = read_csv(dataset)
    X, tlabels = split_class_from_features(corpus)
    classify(X, tlabels, dataset.replace('_features.csv', '_results.txt'))


main()
